# -*- coding: utf-8 -*-
"""
SocketMessageServer inherits SocketMessage and is used by the server
to communicate with socket client via SocketMessageClient

Created on Mon Jun 7 23:47:19 2021

@author: D. Jackson
"""

import logging
import re
import selectors
import socket
import threading
import time
import traceback
from enum import IntEnum, auto, IntFlag
from sys import platform
from typing import Union, Dict, Tuple, List

from .check_windows_esc import _check_windows_esc
from .Command_factory import create_command_mv
from .exceptions import (MultiPyVuError,
                         ClientCloseError,
                         ServerCloseError,
                         PwinComError,
                         SocketError,
                         PythoncomImportError,
                         )
from .IEventManager import Publisher as _Publisher
from .IEventManager import IObserver as _IObserver
from .instrument import Instrument
from .project_vars import SERVER_NAME, CLOCK_TIME
from .SocketMessage import Message


if platform == 'win32':
    try:
        from .exceptions import pywin_com_error
        import pythoncom
        import pywintypes
    except ImportError:
        raise PythoncomImportError


class ServerStatus(IntEnum):
    closed = auto()
    idle = auto()
    connected = auto()


def catch_thread_error(func):
    """
    This decorator is used to catch an error within a function
    """
    def error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # ignore the errors handled in _exit()
        except (
            KeyboardInterrupt,
            MultiPyVuError,
            UserWarning,
            ClientCloseError,
            SocketError,
                ):
            pass
        except BaseException:
            name = threading.current_thread().name
            msg = f'Exception in thread \'{name}\' '
            msg += f'in method \'{func.__name__}\':\n'
            msg += traceback.format_exc()
            logger = logging.getLogger(SERVER_NAME)
            logger.info(msg)
    return error_handler


class ServerMessage(Message, threading.Thread, _Publisher):
    """
    This class is used by the Server to send and receive messages through
    the socket connection and respond to the Client's request.

    It inherits the Message base class, threading.Thread, and the
    Publisher class.

    Parameters:
    -----------
    instr: Instrument
        holds information about communications with MultiVu
    selector: selectors.DefaultSelector
        the selector object
    socket_timeout: float, or None
        define the length of time before the socket times out.  A value
        of None means it will never timeout.
    port: int
        the port number.
    """
    class ClientType(IntFlag):
        listening = auto()
        read_write = auto()
        other = auto()
    # bite wise or all of the enum options
    _all_client_types = ClientType.listening \
        | ClientType.read_write \
        | ClientType.other

    def __init__(self,
                 instr: Instrument,
                 selector: selectors.DefaultSelector,
                 socket_timeout: Union[float, None],
                 port: int,
                 ):
        threading.Thread.__init__(self)
        Message.__init__(self, socket_timeout)
        _Publisher.__init__(self)

        self.name = SERVER_NAME
        self.daemon = True

        self._cl_type = ServerMessage.ClientType
        self._start_called = False

        self.selector = selector
        self.port = port
        self.addr = ('0.0.0.0', self.port)
        self.instr = instr
        self.verbose = instr.verbose
        self.scaffolding = instr.scaffolding_mode
        self.server_threading = instr.run_with_threading
        self.logger = logging.getLogger(SERVER_NAME)
        self.mutex = threading.Lock()
        self.server_status: ServerStatus = ServerStatus.idle
        # keep track of the read/write selectors when 'START' is received
        self._main_selectors: Dict[socket.socket,
                                   'ServerMessage.ClientType'] = {}
        self._stop_flag = False

    #########################################
    #
    # Private Methods
    #
    #########################################

    def _config_sock(self) -> socket.socket:
        """
        Configure the socket and selectors

        Returns:
        --------
        Configured socket
        """
        # Set up the sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('0.0.0.0', self.port))
        except socket.error as e:
            if e.strerror == 'Address already in use':
                msg = f'{e.strerror}: try using a different '
                msg += f'port (used {self.port})'
                self.logger.info(msg)
                raise SocketError(msg)
        sock.listen()
        sock.setblocking(False)
        self.server_status = ServerStatus.idle
        self.notify_observers()
        return sock

    def _accept_wrapper(self, sock: socket.socket) -> None:
        """
        This method accepts a new client.
        """
        # get the sock to be ready to read
        accepted_sock, self.addr = sock.accept()
        accepted_sock.setblocking(False)
        self.selector.register(accepted_sock,
                               selectors.EVENT_READ,
                               self._do_work,
                               )
        # decide in ._do_work() whether to change the ClientType
        with self.mutex:
            self._main_selectors[accepted_sock] = self._cl_type.other
            self.server_status = ServerStatus.idle
        self.notify_observers()

    def _do_work(self, sock: socket.socket):
        """
        After ._accept_wrapper is called, it sets this method to be called
        next.  This method reads the socket, deals with what it found, then
        writes the result to the socket and finally prepares the class for the
        next incoming command.

        Parameters:
        -----------
        sock: socket.socket
            The socket connection
        """
        # read sockets
        try:
            self._read(sock)
        except ClientCloseError:
            # This is thrown if the server or the client shut down. If
            # the client shuts down, the server should just keep waiting
            # for a new client to appear, so nothing happens
            pass

        self._process_data(sock.getsockname())

        if self.request:
            if not self.response_created:
                self._process_content()
        self._write(sock)
        # Close when the buffer is drained. The response has been sent.
        # Note that the Message class only handles one message per connection,
        # so after the response is written there is nothing left to do.
        if self._sent_success and not self._send_buffer:
            if self._check_start():
                if self._start_called:
                    with self.mutex:
                        self._main_selectors[sock] = self._cl_type.read_write
                else:
                    self.selector.unregister(sock)
                    sock.close()
                    with self.mutex:
                        del self._main_selectors[sock]
                    # since we got here because a 2nd client
                    # tried to connect, let's reset the _start_called
                    # flag to True
                    self._start_called = True
                self.notify_observers()
            elif self._check_exit():
                self.stop_message()
                self.shutdown()
                raise ServerCloseError('Close server')
            elif self._check_close():
                types = self._cl_type.read_write | self._cl_type.other
                self.unregister_and_close_sockets(types)
                self.notify_observers()
            elif self._check_alive_cmd():
                self.unregister_and_close_sockets(self._cl_type.other)
                self.notify_observers()
            elif self._check_status_cmd():
                self.unregister_and_close_sockets(self._cl_type.other)
                self.notify_observers()

            self._reset_read_state()

    def _get_listen_sock(self) -> socket.socket:
        """
        Uses the selectors information to get the client socket info
        """
        with self.mutex:
            for s, t in self._main_selectors.items():
                if t == self._cl_type.listening:
                    return s
        # if it gets here, then the listening sock was not defined
        raise MultiPyVuError('No listening socket defined')

    def _poll_connections(self):
        """
        Pings the non-listening sockets to ensure they are still active.
        If they are inactive, it closes the socket and removes it from the
        _main_selectors dict.
        """
        for sel_obj in list(self.selector.get_map().values()):
            conn = sel_obj.fileobj
            if isinstance(conn, socket.socket) \
                    and conn != self._get_listen_sock():
                try:
                    conn.sendall(b'PING')
                    conn.recv(1, socket.MSG_PEEK)
                except (ConnectionResetError,
                        ConnectionAbortedError,
                        BrokenPipeError,
                        BlockingIOError):
                    self.selector.unregister(conn)
                    self.close(conn)
                    with self.mutex:
                        del self._main_selectors[conn]

    def _reset_read_state(self):
        """
        Set the json_header_len to None, reset the json_header and
        request dictionaries to {}, and set _request_is_text, _sent_success,
        and .response_created to False
        """
        self._json_header_len = 0
        self.json_header = {}
        self.request = {}
        self._sent_success = False
        self.response_created = False

    def _process_data(self, addr: Tuple[str, int]):
        """
        The data is transferred with a header that starts with two bytes
        which gives the length of the rest of the header (the header also
        has variable length).  The last section contains the data. Each
        of these are processed one at a time, and the buffer, which is
        stored in self._recv_buffer, is trimmed after each state is looked
        at so that by the end, self._recv_buffer just holds the data (action,
        request, and response).
        """

        if self._json_header_len == 0:
            self._process_proto_header()

        if self._json_header_len > 0:
            if self.json_header == {}:
                self._process_json_header()

        if self.json_header != {}:
            if self.request == {}:
                self._process_request(addr)

    def _process_request(self, addr: Tuple[str, int]):
        """
        This takes data in the ._recv_buffer and puts it into the
        JSON formatted .request
        """
        # read the buffer into 'data'
        content_len = self.json_header['content-length']
        if len(self._recv_buffer) < content_len:
            return

        data = self._recv_buffer[:content_len]
        encoding = self.json_header['content-encoding']

        # clear the request from the buffer
        self._recv_buffer = self._recv_buffer[content_len:]

        # process 'data'
        content = self._json_decode(data, encoding)
        action = content['action']
        query = content['query']
        self.request = self.create_request(action, query)
        self._log_received_result(addr, repr(self.request["content"]))

    def _process_content(self):
        """
        THis takes the .request dictionary and figures out what to do with the
        'content' key
        """
        content = self.request['content']
        action = content['action']
        query = content['query']
        result = ''

        default_result = f'Connected to {self.instr.name} '
        default_result += f'MultiVuServer at {self.addr}'
        if action == 'START':
            # check if a client is already connected
            if self._start_called:
                result = 'Connection attempt rejected from '
                result += f'{self.addr}: another client is connected.'
                self.logger.info(result)
                self.request['content']['query'] = result
                self._start_called = False
            else:
                result = default_result
                # change the query to let the client know server info
                query = self._start_to_str()
                self.logger.info(f'Accepted connection from {self.addr}')
                self.server_status = ServerStatus.connected
                self._start_called = True
        elif action == 'ALIVE':
            result = default_result
            # Use the query to confirm the command was sent and received
            query = action
        elif action == 'STATUS':
            result = self.server_status.name
            # Use the query to confirm the command was sent and received
            query = action
        elif action == 'EXIT':
            # Use the query to confirm the command was sent and received
            result = 'Closing client and exiting server.'
            query = action
            self.logger.info(result)
        elif action == 'CLOSE':
            result = f'Client {self.addr} disconnected.'
            # Use the query to confirm the command was sent and received
            query = action
            self.logger.info(result)
        else:
            command = f'{action} {query}'
            try:
                result = self._do_request(command)
            except MultiPyVuError as e:
                result = e.value
            except ValueError:
                result = f"The command '{action}' has not been implemented."
        response_content = {'action': action,
                            'query': query,
                            'result': result,
                            }

        self.response = self._create_response_json_content(response_content)
        self.response_created = True
        self._send_buffer += self._create_message(**self.response)

    def _do_request(self, arg_string: str, attempts: int = 0) -> str:
        """
        This takes the arg_string parameter to create a query for
        CommandMultiVu.

        Parameters:
        -----------
        arg_string: str
            The string has the form:
                arg_string = f'{action} {query}'
            For example, if asking for the temperature, the query is blank:
                arg_string = 'TEMP? '
            Or, if setting the temperature:
                arg_string = 'TEMP set_point,
                              rate_per_minute,
                              approach_mode.value'
            The easiest way to create the query is to use:
                ICommand.prepare_query(set_point,
                                       rate_per_min,
                                       approach_mode,
                                       )
        attempts: int (optional, default = 0)
            The number of times this method has been called

        Returns:
        --------
        str
            The return string is of the form:
            '{action}?,{result_string},{units},{code_in_words}'

        """
        split_string = r'([A-Z]+)(\?)?[ ]?([ :\-?\d.,\w]*)?'
        # this returns a list of tuples - one for each time
        # the groups are found.  We only expect one command,
        # so only taking the first element
        [command_args] = re.findall(split_string, arg_string)
        try:
            cmd, question_mark, params = command_args
            query = (question_mark == '?')
        except IndexError:
            return f'No argument(s) given for command {command_args}.'
        else:
            mvu_commands = create_command_mv(self.instr.name,
                                             self.instr.multi_vu)
            max_retries = 5
            try:
                if query:
                    return mvu_commands.get_state(cmd, params)
                else:
                    return mvu_commands.set_state(cmd, params)
            except (pythoncom.com_error,
                    pywintypes.com_error,
                    AttributeError,
                    ) as e:
                if attempts < max_retries:
                    attempts += 1
                    msg = 'pythoncom.com_error attempt number: '
                    msg += f'{attempts}'
                    self.logger.debug(msg)
                    self.instr.end_multivu_win32com_instance()
                    time.sleep(CLOCK_TIME)
                    self.instr.get_multivu_win32com_instance()
                    return self._do_request(arg_string, attempts)
                else:
                    raise MultiPyVuError(str(e))

    #########################################
    #
    # Public Methods
    #
    #########################################

    def run(self):
        """
        This method is run when ServerMessage.start() is called. It stops any
        currently running threads, then calls .monitor_socket_connection().
        Once that method has completed, it calls .shutdown()
        """
        self.stop_message(False)
        self.monitor_socket_connection()
        self.shutdown()

    def stop_message(self, set_stop: bool = True):
        """
        Stops this class from running as a thread.

        Parameters:
        -----------
        set_stop: bool (optional)
            True (default) will stop the thread
        """
        with self.mutex:
            self._stop_flag = set_stop

    def stop_requested(self) -> bool:
        """
        Queries this class to see if it has been asked to stop the thread
        """
        return self._stop_flag

    @catch_thread_error
    def monitor_socket_connection(self):
        """
        This monitors traffic and looks for new clients and new requests.
        It configures the socket connection, registers the
        selectors and gets a win32com instance to talk to MultiVu.

        It then enters a loop to monitor the traffic.  For new clients, it
        calls ._accept_wrapper().  After that, it uses ._do_work() to figure
        out how to implement the client's request.
        """
        # we can never get to this point without Instrument being instantiated
        if self.instr is None:
            err_msg = 'The class, Instrument, was not instantiated'
            raise MultiPyVuError(err_msg)

        listening_sock = self._config_sock()
        with self.mutex:
            self._main_selectors[listening_sock] = self._cl_type.listening
        # Register the server socket with the selector to
        # monitor for incoming connections
        self.selector.register(listening_sock,
                               selectors.EVENT_READ,
                               self._accept_wrapper,
                               )
        self.logger.info(f'Listening on port {self.port}')

        # we can never get to this point without Instrument being instantiated
        if self.instr is None:
            err_msg = 'The class, Instrument, was not instantiated'
            raise MultiPyVuError(err_msg)

        # Connect to MultiVu in order to enable a new thread,
        # but only if the connection has not yet been made (allows
        # for multiple consecutive client connections).
        self.instr.get_multivu_win32com_instance()

        while True:
            _check_windows_esc()
            if self.stop_requested():
                break
            # If the server is going to check the connections, it needs
            # a timer so that it only checks connections every xxx seconds
            # self._poll_connections()

            try:
                events = self.selector.select(timeout=self._socket_timeout)
            except SocketError:
                # This error happens if the selectors is unavailable.
                continue
            for key, mask in events:
                # This is the data we passed to `register`
                # It is ._accept_wrapper() the first time,
                # then ._do_work() the next time
                work_method = key.data
                sock = key.fileobj
                try:
                    work_method(sock)
                except BlockingIOError:
                    # try calling this method again
                    time.sleep(CLOCK_TIME)
                    continue
                except MultiPyVuError as e:
                    self.logger.info(e)
                    break
                except ServerCloseError:
                    self.stop_message()
                    break
                except ClientCloseError as e:
                    self.logger.info(e)
                    self.stop_message()
                    break
                except ConnectionAbortedError as e:
                    self.logger.info(e)
                    self.stop_message()
                    break
                except AttributeError as e:
                    msg = 'Lost connection to socket.'
                    self.logger.info(f'{msg}:   AttributeError: {e}')
                    tb_str = ''.join(traceback.format_exception(None,
                                                                e,
                                                                e.__traceback__,
                                                                )
                                     )
                    self.logger.info(tb_str)
                    self.stop_message()
                    break
                except pywin_com_error as e:
                    self.logger.info(str(PwinComError(e)))
                    self.stop_message()
                    break
                except KeyboardInterrupt as e:
                    raise e

    def connection_good(self, sock: Union[socket.socket, None]) -> bool:
        """
        Calls selectors.get_key(socket) to see if the connection is good.
        """
        if not sock:
            return False
        try:
            # Check for a socket being monitored to continue.
            self.selector.get_key(sock)
            return True
        except (ValueError, KeyError):
            # can get ValueError if self.sock is None
            # KeyError means no selector is registered
            return False

    def unregister_and_close_sockets(self,
                                     types: Union['ServerMessage.ClientType',
                                                  None] = None,
                                     ) -> None:
        """
        Unregister and close connections in the types variable.

        Parameters:
        -----------
        types: ServerMessage.ClientType or None
            Default: None (all ClientTypes)
            This can have a bit-wise input using the logical or
            for multiple types.
        """
        types = ServerMessage._all_client_types if types is None else types
        # In normal situations, this list has two items, one for
        # _accept_wrapper() and another for read()
        selectors_to_delete = []
        for key, sel_obj in list(self.selector.get_map().items()):
            fileobj = sel_obj.fileobj
            if isinstance(fileobj, socket.socket):
                conn: socket.socket = fileobj
                method = sel_obj.data
                if method is not None:
                    default_type = self._cl_type.other
                    with self.mutex:
                        cl_type = self._main_selectors.get(conn, default_type)
                    if cl_type & types:
                        self.selector.unregister(conn)
                        conn.close()
                        selectors_to_delete.append(conn)
        for s in selectors_to_delete:
            with self.mutex:
                del self._main_selectors[s]
        if self.num_connected() > 0:
            self.server_status = ServerStatus.connected
        else:
            self.server_status = ServerStatus.idle
            self._start_called = False

    def shutdown(self):
        """
        Unregister the Selector and close the socket
        """
        # since we are exiting, need to unregister all selectors
        self.unregister_and_close_sockets(ServerMessage._all_client_types)
        self.server_status = ServerStatus.closed
        self.notify_observers()

    def num_connected(self) -> int:
        """
        Use the _main_selectors dictionary to count the
        number of clients connected.  Does not include the
        listening socket in the tally.
        """
        connections = 0
        with self.mutex:
            for t in self._main_selectors.values():
                connections += 1 if t != self._cl_type.listening else 0
        return connections

    def is_client_connected(self) -> bool:
        """
        Uses .num_connected to see if a client is connected to the server
        """
        # use the number of connections to see if anyone is connected
        return self.num_connected() > 0

    def transfer_observers(self) -> List[_IObserver]:
        """
        Unsubscribe and transfer the observers
        """
        outgoing_list = []
        for obs in self._observers:
            self.unsubscribe(obs)
            outgoing_list.append(obs)
        return outgoing_list
