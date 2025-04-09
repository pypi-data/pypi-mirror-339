#!/usr/bin/env python3
"""
Created on Mon Jun 7 23:47:19 2021

MultiVuClient_base.py is a module for use on a network that has access to a
computer running MultiVuServer.py.  By running this client, a python script
can be used to control a Quantum Design cryostat.

This is the base class.  It has the basic communication commands.  The
MultiVuClient class has specific commands to be used with this class.

@author: D. Jackson
"""

import logging
import sys
import traceback
from socket import timeout as sock_timeout
from time import sleep
from typing import Dict, Union

from .__version import __version__ as mpv_version
from .exceptions import (ClientCloseError, MultiPyVuError, ServerCloseError,
                         SocketError)
from .logging_config import remove_logs, setup_logging
from .project_vars import (CLIENT_NAME, CLOCK_TIME, HOST_CLIENT, PORT,
                           TIMEOUT_LENGTH)
from .SocketMessageClient import ClientMessage as _ClientMessage

MAX_TRIES = 3


class ClientBase():
    """
    This class is used for a client to connect to a computer with
    MultiVu running MultiVuServer.py.

    Parameters
    ----------
    host: str (optional)
        The IP address for the server.  Default is 'localhost.'
    port: int (optional)
        The port number to use to connect to the server.
    socket_timeout: float, None (optional)
        The time in seconds that the client will wait to try
        and connect to the server.  Value of None will wait
        indefinitely.  Default is project_vars.TIMEOUT_LENGTH
    """

    def __init__(self,
                 host: str = HOST_CLIENT,
                 port: int = PORT,
                 socket_timeout: Union[float, None] = TIMEOUT_LENGTH,
                 ):
        self.address = (host, port)
        self._socket_timeout = socket_timeout
        self._message = None     # ClientMessage object
        self._instr = None
        self.instrument_name = ''

    def __enter__(self):
        """
        The class can be started using context manager terminology
        using 'with.' This connects to a running MultiVuServer.

        Raises
        ------
        ConnectionRefusedError
            This is raised if there is a problem connecting to the server. The
            most common issue is that the server is not running.

        Returns
        -------
        Reference to this class

        """
        # Configure logging
        setup_logging(True)
        self._logger = logging.getLogger(CLIENT_NAME)
        if not self._message:
            self._message = _ClientMessage(self.address, self._socket_timeout)
        try:
            self._message.connect_to_socket()
        except (sock_timeout, ConnectionRefusedError) as e:
            msg = 'Could not connect to the server.  Please ensure the '
            msg += 'server is running, it is not already connected to another '
            msg += 'client, and the address matches '
            msg += f'(using {self.address}).'
            self._logger.info(msg)
            e.args = (msg,)
            raise self.__exit__(*sys.exc_info())
        except BaseException:
            raise self.__exit__(*sys.exc_info())
        self._logger.debug(f'MultiPyVu Version: {mpv_version}')
        self._logger.info(f'Starting connection to {self.address}')
        # send a request to the sever to confirm a connection
        action = 'START'
        response = self._query_server(action)

        if response is None:
            raise MultiPyVuError('Keyboard interrupt')

        self._logger.info(response['result'])
        self._instr = self._message.instr
        self.instrument_name = self._message.instr.name
        # self._log_event.show_logger_name(self._instr.run_with_threading)
        ver = self.get_version()
        if ver != mpv_version:
            self._query_server('CLOSE')
            msg = 'MultiPyVu Server and Client must be running '
            msg += 'the same versions:\n'
            msg += f'\tMultiPyVu.Server: ({ver})\n'
            msg += f'\tMultiPyVu.Client: ({mpv_version})'
            self.__exit__(SystemExit,
                          SystemExit(msg),
                          sys.exc_info()[2])
        self.address = self._message.addr
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> BaseException:
        """
        Because this class is a context manager, this method is called when
        exiting the 'with' block.  It cleans up all of the connections and
        deals with errors that may have arrived.

        Parameters:
        -----------
        exc_type, exc_value, exc_traceback make up the tuple returned
        by sys.exc_info()
        """
        send_close = True
        # Error handling
        if isinstance(exc_value, SystemExit):
            remove_logs(self._logger)
            logging.shutdown()
            raise exc_value
        elif isinstance(exc_value, KeyboardInterrupt):
            self._logger.info('Caught keyboard interrupt, exiting')
        elif isinstance(exc_value, ServerCloseError):
            msg = 'Shutting down the server.'
            self._logger.info(msg)
            send_close = False
        elif isinstance(exc_value, ConnectionRefusedError):
            # Note that ServerCloseError (ConnectionAbortedError) and
            # ConnectionRefusedError are subclasses of
            # ClientCloseError (ConnectionError)
            send_close = False
            # brief pause to let the server close
            sleep(CLOCK_TIME)
        elif isinstance(exc_value, ClientCloseError):
            # Note that ServerCloseError (ConnectionAbortedError) and
            # ConnectionRefusedError are subclasses of
            # ClientCloseError (ConnectionError)
            send_close = False
            sleep(CLOCK_TIME)
        elif isinstance(exc_value, TimeoutError):
            send_close = False
        elif isinstance(exc_value, sock_timeout):
            send_close = False
        elif isinstance(exc_value, SocketError):
            send_close = False
        elif isinstance(exc_value, ValueError):
            pass
        elif isinstance(exc_value, MultiPyVuError):
            self._logger.info(exc_value)
        elif isinstance(exc_value, BaseException):
            msg = 'MultiVuClient: error: exception for '
            msg += f'{self.address}:'
            msg += f'\n{traceback.format_exc()}'
            self._logger.info(msg)

            remove_logs(self._logger)
            logging.shutdown()

            # Prior to v2.3.0, this section of the code would force it
            # to quit.  But starting with 2.3.0, it just returns the error
            #
            # using os._exit(0) instead of sys.exit(0) because we need
            # all threads to exit, and we don't know if there will be
            # threads running.  os._exit(0) is more forceful, but in
            # this case everything is wrapped up when calling
            # this method.  Note that this can not clean up anything
            # from other threads, though. If one goes back to quitting,
            # create exit codes to help show why the script quit
            # os._exit(0)

            raise exc_value

        if self._message is not None:
            if send_close:
                # tell the server we are exiting
                try:
                    self._query_server('CLOSE')
                except BaseException:
                    # ignore any error here and just keep going
                    pass
            self._message = None
        remove_logs(self._logger)
        logging.shutdown()
        self._instr = None
        self.instrument_name = ''
        return exc_value

    ###########################
    #  Client Methods
    ###########################

    def open(self):
        """
        This is the entry point into the MultiVuClient.  It connects to
        a running MultiVuServer

        Raises
        ------
        ConnectionRefusedError
            This is raised if there is a problem connecting to the server. The
            most common issue is that the server is not running.

        Returns
        -------
        A reference to this class

        """
        return self.__enter__()

    def close_client(self):
        """
        This command closes the client, but keeps the server running
        """
        # tell the server we are exiting
        self._query_server('CLOSE')

    def __close_and_exit(self) -> BaseException:
        """
        calls the __exit__() method
        """
        err_info = sys.exc_info()
        return self.__exit__(*err_info)

    def close_server(self):
        """
        This command closes the server
        """
        self._query_server('EXIT')

    def get_version(self) -> str:
        """
        Returns the version number
        """
        if self._message:
            return self._message.server_version
        else:
            return mpv_version

    def force_quit_server(self) -> str:
        """
        Forces the MultiPyVu.Server to quit.  This is especially useful if
        something happens to the server and it remains open after the script
        closes.

        Returns:
        --------
        Response from quitting the server. Successfully quitting the client
        results in 'Quit the server at (<ip_address>, <port>)'
        """
        if self._message is None:
            message = _ClientMessage(self.address, self._socket_timeout)
            rtrn_msg = f'Quit the server at {message.addr}'
            try:
                message.connect_to_socket()
                message.send_and_receive('EXIT')
            except ServerCloseError:
                # this is expected
                pass
            except (
                    sock_timeout,
                    ConnectionRefusedError,
                    TimeoutError,
                    SocketError,
                    MultiPyVuError,
                    ):
                rtrn_msg = 'Could not connect to the server at '
                rtrn_msg += f'{self.address}).'
            message.socket.close()
        else:
            try:
                self._query_server('EXIT')
            except (
                    ConnectionAbortedError,
                    ServerCloseError,
                    ):
                rtrn_msg = f'Quit the server at {self.address}'
            except BaseException as e:
                tb_str = ''.join(traceback.format_exception(None,
                                                            e,
                                                            e.__traceback__,
                                                            )
                                 )
                rtrn_msg = tb_str
        return rtrn_msg

    def is_server_running(self) -> bool:
        """
        Queries the MultiVuServer to see if it is running.

        Returns:
        --------
        True (False) if the server is running (not running).
        """
        if self._message is None:
            message = _ClientMessage(self.address, self._socket_timeout)
            try:
                message.connect_to_socket()
                response = message.send_and_receive('ALIVE', '?')
            except (
                    sock_timeout,
                    ConnectionRefusedError,
                    TimeoutError,
                    SocketError,
                    MultiPyVuError,
                    ):
                return False
            message.socket.close()
        else:
            response = self._query_server('ALIVE', '?')

        return response['action'] == 'ALIVE'

    def get_server_status(self) -> str:
        """
        Queries the MultiVuServer for its status.

        Returns:
        --------
        string indicating the server status
        """
        response = {'result': 'closed'}
        if self._message is None:
            message = _ClientMessage(self.address, self._socket_timeout)
            try:
                message.connect_to_socket()
                response = message.send_and_receive('STATUS')
            except (
                    sock_timeout,
                    ConnectionRefusedError,
                    TimeoutError,
                    SocketError,
                    MultiPyVuError,
                    ):
                pass
            message.socket.close()
        else:
            response = self._query_server('STATUS')
        return response['result']

    def _query_server(self,
                      action: str,
                      query: str = '',
                      ) -> Dict[str, str]:
        """
        Queries the server using the action and query parameters.

        Parameters
        ----------
        action : str
            The general command going to MultiVu:  TEMP(?), FIELD(?), and
            CHAMBER(?), etc..  If one wants to know the value of the action,
            then it ends with a question mark.  If one wants to set the action
            in order for it to do something, then it does not end with a
            question mark.
        query : str, optional
            The query gives the specifics of the command going to MultiVu.  For
            queries. The default is '', which is what is used when the action
            parameter ends with a question mark.

        Returns:
        --------
        The response dictionary from the ClientMessage class.
        """
        resp = {}
        if self._message is None:
            raise SocketError('Client not connected to the server')
        try:
            resp: dict = self._message.send_and_receive(action, query)
        except MultiPyVuError:
            raise self.__close_and_exit()
        except ServerCloseError:
            self.__close_and_exit()
        except ClientCloseError as e:
            self.close_client()
            resp['action'] = action
            resp['query'] = ''
            resp['result'] = e.args
        except SocketError as e:
            self.__close_and_exit()
            if action in [
                    'ALIVE',
                    'STATUS',
                    ]:
                # set the response action
                resp['action'] = ''
                resp['result'] = 'closed'
            else:
                self._logger.info(e.args[0])
                sys.exit(0)
        # except ConnectionRefusedError:
        #     resp['action'] = ''
        except TimeoutError as e:
            # this includes ClientCloseError, ServerCloseError,
            # and TimeoutError
            self._logger.info(e)
            self.__close_and_exit()
            sys.exit(0)
        except KeyboardInterrupt:
            self.close_client()
            sys.exit(0)
        except Exception:
            self.__close_and_exit()
        return resp
