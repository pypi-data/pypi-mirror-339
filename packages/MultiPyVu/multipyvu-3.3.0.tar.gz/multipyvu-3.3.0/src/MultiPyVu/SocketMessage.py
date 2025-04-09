# -*- coding: utf-8 -*-
"""
SocketMessage.py is the base class for sending information across sockets.  It
has two inherited classes, SocketMessageServer.py and SocketMessageClient.py

Created on Mon Jun 7 23:47:19 2021

@author: D. Jackson
"""

import io
import json
import logging
import re
import socket
import struct
import sys
import traceback
from abc import ABC
from typing import Dict, Tuple, Union

from .__version import __version__ as mpv_version
from .exceptions import ClientCloseError, SocketError
from .project_vars import PORT


class Message(ABC):
    def __init__(self, socket_timeout: Union[float, None]):
        """
        This is the base class for holding data when sending or receiving
        sockets.  The class is instantiated by Server() and
        Client().

        The data is sent (.request['content']) and received
        (.response['content']) as a dictionary of the form:
                action (ie, 'TEMP?', 'FIELD',...)
                query
                result

        The information goes between sockets using the following format:
            Header length in bytes
            JSON header (.json_header) dictionary with keys:
                byteorder
                content-type
                content-encoding
                content-length
            Content dictionary with key:
                action
                query
                result

        Parameters:
        -----------
        socket_timeout : float, None
            The socket timeout in seconds.  None means indefinite timeout.

        """
        self._socket_timeout = socket_timeout
        self.logger = logging      # this is defined in the child classes
        self.port = PORT
        self.addr: Tuple[str, int]
        self.request: dict = {}
        self.response: dict = {}
        self._recv_buffer = b''
        self._send_buffer = b''
        self._request_queued = False     # only used by the client
        self._json_header_len: int = 0
        self.json_header = {}
        self.response_created = False    # only used by the server
        self._sent_success = False       # only used by the server
        self.mvu_flavor = None
        self.verbose = False
        self.scaffolding = False
        self.server_threading = False
        self.server_version = 'unknown server version'

    #########################################
    #
    # Private Methods
    #
    #########################################

    def _start_to_str(self) -> str:
        """
        Converts flags noting configuration parameters into a string.
        """
        query_list = []
        # add the version number
        query_list.append(mpv_version)
        if self.verbose:
            query_list.append('v')
        if self.scaffolding:
            query_list.append('s')
        if self.server_threading:
            query_list.append('t')
        return ';'.join(query_list)

    def _str_to_start_options(self, server_options: str) -> Dict:
        """
        Converts a string noting configuration parameters into flags

        Returns:
        --------
        Dict: key = option name, value = option flag (str)
        """
        options_list = server_options.split(';')
        options_dict = {}
        # find the server version number
        for option in options_list:
            search = r'([0-9]+.[0-9]+.[0-9]+)'
            v_list = re.findall(search, option)
            # check that it found a version number
            if len(v_list) == 1:
                options_dict['version'] = v_list[0]
            break
        options_dict['verbose'] = 'v' in options_list
        options_dict['scaffolding'] = 's' in options_list
        options_dict['threading'] = 't' in options_list
        return options_dict

    def _read(self, sock: socket.socket):
        """
        Reads the socket and loads it into the ._recv_buffer

        Raises:
        -------
        ClientCloseError if the server closed the connection
            or if the data received from the socket is none.
        SocketError if a socket was aborted
        """
        try:
            # Should be ready to read
            data = sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        except ConnectionResetError:
            raise ClientCloseError('Server closed the connection')
        except ConnectionAbortedError:
            msg = 'An established connection was aborted.'
            raise SocketError(msg)
        else:
            if data:
                self._recv_buffer += data
            else:
                raise ClientCloseError('Close client')

    def _write(self, sock: socket.socket):
        """
        Writes data via a socket.  Sets the ._sent_success flag.

        Raises:
        -------
        SocketError if there is no socket connection
        """
        # until the sock is sent, this flag should be False
        self._sent_success = False

        if self._send_buffer:
            try:
                # Should be ready to write
                sent = sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                self._sent_success = False
            except BrokenPipeError:
                # Resource temporarily unavailable
                self._sent_success = False
            # Note that socket.error = OSError, which is a base class with
            # the following subclasses:
            # ClientCloseError (ConnectionError)
            # ServerCloseError (ConnectionAbortedError)
            # ConnectionRefusedError
            except socket.error:
                # No socket connection
                self._sent_success = False
                err_msg = 'No socket connection.  Please make sure '
                err_msg += 'MultiVuServer is running, that '
                err_msg += 'MultiVuClient is using the same IP address, '
                err_msg += 'that the IP address is correct, that the server '
                err_msg += 'can accept connections, etc.'
                raise SocketError(err_msg)
            else:
                self._log_send(sock.getpeername())
                self._sent_success = True
                self._send_buffer = self._send_buffer[sent:]

    def _log_received_result(self, addr: Tuple[str, int], message: str):
        """
        Helper tool to add an entry to the log for the message received
        """
        msg = f';from {addr}; Received request {message}'
        self.log_message(msg)

    def _log_send(self, addr: Tuple[str, int]):
        """
        Helper tool to add an entry to the log for the message being sent
        """
        msg = f';to {addr}; Sending {repr(self._send_buffer)}'
        self.log_message(msg)

    def _check_start(self) -> bool:
        """
        Checks to see if the client has requested to make a connection

        Returns:
        --------
        Bool: True means 'START' was requested
        """
        start_sent = self.response['content']['action'] == 'START'
        start_received = self.request['content']['action'] == 'START'
        return start_sent and start_received

    def _check_close(self) -> bool:
        """
        Checks to see if the client has requested to close the connection
        to the server.

        Returns:
        --------
        Bool: True if CLOSE was called
        """
        close_sent = self.response['content']['action'] == 'CLOSE'
        closing_received = self.response['content']['query'] == 'CLOSE'
        return close_sent and closing_received

    def _check_exit(self) -> bool:
        """
        Checks to see if the client has requested to exit the program, meaning
        the client closes the connection and the server exits

        Returns:
        --------
        Bool: True means 'EXIT' was requested
        """
        exit_sent = self.response['content']['action'] == 'EXIT'
        exit_received = self.response['content']['query'] == 'EXIT'
        return exit_sent and exit_received

    def _check_alive_cmd(self) -> bool:
        """
        Checks to see if the client has requested to see if the
        server is running

        Returns:
        --------
        Bool: True if ALIVE was called
        """
        alive_sent = self.response['content']['action'] == 'ALIVE'
        alive_received = self.response['content']['query'] == 'ALIVE'
        return alive_sent and alive_received

    def _check_status_cmd(self) -> bool:
        """
        Checks to see if the client has requested to check server status

        Returns:
        --------
        Bool: True if STATUS was called
        """
        status_sent = self.response['content']['action'] == 'STATUS'
        status_received = self.response['content']['query'] == 'STATUS'
        return status_sent and status_received

    def _create_response_json_content(self, content: Dict[str, str],
                                      encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Configures the response given the content.

        Parameters:
        -----------
        content: Dict[str, str]
            the information that goes into the 'content' key
        encoding: str (optional)
            default is 'utf-8'

        Returns:
        --------
        Dict: key = 'type', 'encoding', and 'content'
        """
        response = {
            'type': 'text/json',
            'encoding': encoding,
            'content': content,
        }
        return response

    def _json_encode(self, dict_obj: Dict[str, str],
                     encoding: str = 'utf-8') -> bytes:
        """
        Takes a dictionary and converts it to a JSON formatted byte string

        Parameters:
        -----------
        dict_obj: Dict[str, str]
            A dictionary that needs to be converted
        encoding: str (optional)
            default = 'utf-8

        Returns:
        --------
        bytes: a byte string containing the dict_obj information
        """
        return json.dumps(dict_obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self,
                     json_bytes: bytes,
                     encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Takes a JSON formatted byte string and converts it to a dictionary

        Parameters:
        -----------
        json_bytes: bytes
            A byte string containing the dict_obj information
        encoding: str (optional)
            default = 'utf-8

        Returns:
        --------
        Dict[str, str]: a dictionary made from the input dict_obj
        """
        text_io_wrapper = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(text_io_wrapper)
        text_io_wrapper.close()
        return obj

    def _create_message(self,
                        *,
                        content: Dict[str, str],
                        type: str = 'text/json',
                        encoding: str = 'utf-8') -> bytes:
        """
        Creates the message to be sent across the socket connection.

        Parameters:
        -----------
        * This notes that this method is a keyword only argument so all
            parameters must be named.
        content: Dict[str, str]
            The dictionary of information to be sent
        type: str (optional)
            Default is 'text/json'
        encoding: str (optional)
            Default is 'utf-8'

        Returns:
        --------
        bytes: a binary encoded string made from the input parameters
        """
        content_bytes = self._json_encode(content)
        header = {
            'byteorder': sys.byteorder,
            'content-type': type,
            'content-encoding': encoding,
            'content-length': len(content_bytes),
        }
        header_bytes = self._json_encode(header)
        message_hdr = struct.pack('>H', len(header_bytes))
        message = message_hdr + header_bytes + content_bytes
        return message

    def _process_proto_header(self):
        """
        Reads the ._recv_buffer to find the header and save it to
        ._json_header_len.  This method removes the header info from
        ._recv_buffer.
        """
        header_len = 2
        if len(self._recv_buffer) >= header_len:
            # format = >H, which means:
            #   > = big-endian
            #   H = unsigned short, length = 2 bytes
            # This returns a tuple, but only the first item has a value,
            # which is why the line ends with [0]
            self._json_header_len = struct.unpack(
                '>H',
                self._recv_buffer[:header_len])[0]
            if len(self._recv_buffer) > self._json_header_len:
                # Now that we know how big the header is, we can trim
                # the buffer and remove the header length info
                self._recv_buffer = self._recv_buffer[header_len:]

    def _process_json_header(self):
        """
        This processes ._recv_buffer to get information from the JSON
        header and then remove the header from ._recv_buffer.
        """
        header_len = self._json_header_len

        # The buffer holds the header and the data.  This makes sure
        # that the buffer is at least as long as we expect.  It will
        # be longer if there is data.
        if len(self._recv_buffer) >= header_len:
            # parse the buffer to save the header
            try:
                self.json_header = self._json_decode(
                                        self._recv_buffer[:header_len])
            except UnicodeDecodeError as e:
                msg = f'\nFull received buffer = {self._recv_buffer}'
                msg += '\nBuffer sent to ._json_decode = '
                msg += f'{self._recv_buffer[:header_len]}'
                self.log_message(msg)

                original_traceback = traceback.format_exc()
                traceback_with_msg = original_traceback + msg
                raise UnicodeDecodeError(e.encoding,
                                         e.object,
                                         e.start,
                                         e.end,
                                         traceback_with_msg)

            # This ensures that the header has all of the required fields
            for required_header in (
                    'byteorder',
                    'content-length',
                    'content-type',
                    'content-encoding',
                    ):
                if required_header not in self.json_header:
                    msg = f'Missing required header "{required_header}".'
                    raise ValueError(msg)

            # Then cut the buffer down to remove the header so that
            # now the buffer only has the data.
            self._recv_buffer = self._recv_buffer[header_len:]

    #########################################
    #
    # Public Methods
    #
    #########################################

    def log_message(self, msg: str):
        """
        A helper tool to log the socket message.  This uses the
        .verbose flag to decide if it should only log the message
        in the log file, or if it should also print the message.

        Parameters:
        -----------
        msg: str
            The string to be logged
        """
        if self.verbose:
            self.logger.info(msg)
        else:
            self.logger.debug(msg)

    def close(self, sock: socket.socket):
        """
        Close the socket connection
        """
        msg = f'Closing connection to {self.addr}'
        self.logger.info(msg)
        if sock is not None:
            self.addr = sock.getpeername()
            sock.close()

    def create_request(self, action: str, query: str) -> Dict[str, str]:
        """
        Creates the .request dictionary

        Parameters:
        -----------
        action: str
            The action specified by the user
        query: str
            Information that needs to be included for some actions
        """
        self.request = {
            'type': 'text/json',
            'encoding': 'utf-8',
            'content': dict(action=action.upper(), query=query, result=''),
            }
        return self.request
    
    def get_version(self) -> str:
        """
        Returns the version number
        """
        return self.server_version
