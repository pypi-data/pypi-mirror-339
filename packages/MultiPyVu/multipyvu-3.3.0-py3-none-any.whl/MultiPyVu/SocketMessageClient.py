# -*- coding: utf-8 -*-
"""
SocketMessageClient.py inherits SocketMessage and is used by the client
to communicate with socket server via SocketMessageServer

Created on Mon Jun 7 23:47:19 2021

@author: D. Jackson
"""

import logging
import re
import socket
from time import sleep
from typing import Dict, Tuple, Union

from .check_windows_esc import _check_windows_esc
from .exceptions import (ClientCloseError, MultiPyVuError, ServerCloseError,
                         SocketError)
from .instrument import Instrument
from .project_vars import CLIENT_NAME, CLOCK_TIME
from .SocketMessage import Message


class ClientMessage(Message):
    """
    This class is used by the Client to send and receive messages through
    the socket connection and display the Server's response.

    It inherits the Message base class.

    Parameters:
    -----------
    address: Tuple[str, int]
        specify the host address information:  (IP address, port number)
    socket_timeout: float, or None
        define the length of time before the socket times out.  A value
        of None means it will never timeout.
    """
    def __init__(self,
                 address: Tuple[str, int],
                 socket_timeout: Union[float, None],
                 ):
        super().__init__(socket_timeout)
        self.addr = address
        self.logger = logging.getLogger(CLIENT_NAME)

    #########################################
    #
    # Private Methods
    #
    #########################################

    def _process_start(self):
        """
        This helper method is called if START was sent and received.  It
        deciphers all of the settings from the Server.
        """
        content = self.response['content']
        too_many = 'Connection attempt rejected from'
        if content['result'].startswith(too_many):
            raise SocketError(content['result'])

        self.addr = self.socket.getsockname()
        options_dict = self._str_to_start_options(content['query'])
        self.server_version = options_dict['version']
        self.verbose = options_dict['verbose']
        self.scaffolding = options_dict['scaffolding']
        self.server_threading = options_dict['threading']
        resp = content.get('result', '')
        search = r'Connected to ([\w]*) MultiVuServer'
        self.mvu_flavor = re.findall(search, resp)[0]
        # the Instrument class is used to hold info and
        # can be instantiated with scaffolding mode so that
        # it does not try to connect with a running MultiVu
        self.instr = Instrument(self.mvu_flavor,
                                True,   # instantiate in scaffolding mode
                                self.server_threading,
                                self.verbose)

    def _queue_request(self):
        """
        Collects everything needed to create the request message for the Server
        """
        content = self.request['content']
        type = self.request['type']
        encoding = self.request['encoding']

        req = {
            'type': type,
            'encoding': encoding,
            'content': content,
        }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def _process_response(self, addr: Tuple[str, int]):
        """
        This decodes the response from the Server
        """
        content_len = self.json_header["content-length"]
        if len(self._recv_buffer) < content_len:
            return

        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        encoding = self.json_header["content-encoding"]
        self.response['content'] = self._json_decode(data, encoding)
        self._log_received_result(addr, repr(self.response))

    def _check_multipyvu_error(self):
        """
        Check for a MultiPyVu error returned from the Server

        Raises:
        -------
        MultiPyVuError
        """
        result: str = self.response['content']['result']
        if result.startswith('MultiPyVuError: '):
            self._reset_read_state()
            raise MultiPyVuError(result)

    def _check_response_answers_request(self) -> None:
        """
        check response answers a request

        Raises:
        -------
        MultiPyVuError if the response does not match the request
        """
        if self.request['content']['action'] != self.response['content']['action']:
            msg = 'Received a response to the '
            msg += 'wrong request:\n'
            msg += f' request = {self.request}\n'
            msg += f'response = {self.response}'
            raise MultiPyVuError(msg)

    def _reset_read_state(self):
        """
        Sets the JSON header length to zero and makes .json_header and
        .request empty dictionaries.
        """
        self._json_header_len = 0
        self.json_header = {}
        self.request = {}

    #########################################
    #
    # Public Methods
    #
    #########################################

    def connect_to_socket(self):
        """
        Define the socket, set the timeout, and make a connection to .addr
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self._socket_timeout)
        self.socket.connect(self.addr)

    def send_and_receive(self,
                         action: str,
                         query: str = '') -> Dict[str, str]:
        """
        This takes an action and a query, and sends it to
        ._monitor_and_get_response() to let that method figure out what
        to do with the information.

        Parameters:
        -----------
        action : str
            The general command going to MultiVu, for example TEMP(?),
            FIELD(?), and CHAMBER(?).  If one wants to know the value
            of the action, then it ends with a question mark.  If one
            wants to set the action in order for it to do something,
            then it does not end with a question mark.
        query : str, optional
            The query gives the specifics of the command going to MultiVu.
            For queries. The default is '', which is what is used when the
            action parameter ends with a question mark.

        Returns:
        --------
        Message.response['content']: Dict
            The information retrieved from the socket and interpreted by
            SocketMessageClient class.

        Raises:
        -------
        SocketError if it is unable to write to the server
        ServerCloseError if the Server closed the connection
            or if the data received from the socket is none.
        ClientCloseError if the Client closes the connection.
        """
        # start by clearing self.response
        self.response = {}

        self.create_request(action, query)
        if not self._request_queued:
            self._queue_request()
        try:
            self._write(self.socket)
        except SocketError as e:
            raise SocketError(e.args[0]) from e
        else:
            if self._request_queued:
                if not self._send_buffer:
                    self._request_queued = False
            _check_windows_esc()

        try:
            self.read()
        # except socket.timeout:
        #     self.close()
        except ServerCloseError as e:
            # Client closed the server
            self.close()
            raise ServerCloseError(e.args[0]) from e
        # just let the ClientCloseError be handled by
        # the caller of send_and_receive()
        # except ClientCloseError as e:
        #     # Client closed the client
        #     self.close()
        #     raise ClientCloseError(e.args[0]) from e
        except SocketError as e:
            raise SocketError(e.args[0]) from e
        else:
            _check_windows_esc()
        if self.response == {}:
            msg = 'No return value, which could mean that MultiVu '
            msg += 'is not running or that the connection has '
            msg += 'been closed.'
            raise ClientCloseError(msg)
        return self.response['content']

    def read(self):
        """
        Reads data from the Server and then processes the response
        """
        # read sockets
        while True:
            try:
                self._read(self.socket)
            except socket.timeout:
                # must still be waiting for a response from the server
                _check_windows_esc()
                sleep(CLOCK_TIME)
            except ClientCloseError as e:
                # This is thrown if the server or the client shut down. If
                # the server shuts down, the client needs to also shut down
                if self.request['content']['action'] == 'START':
                    err_msg = 'No connection to the sever upon start.  Is the '
                    err_msg += 'server running?'
                    self.logger.info(err_msg)
                raise ClientCloseError(e.args[0]) from e
            else:
                # no errors, so exit the while-loop
                break

        if self._json_header_len == 0:
            self._process_proto_header()

        if self._json_header_len > 0:
            if self.json_header == {}:
                self._process_json_header()

        if self.json_header:
            self._process_response(self.socket.getsockname())

        self._check_response_answers_request()

        self._check_multipyvu_error()

        if self._check_start():
            self._process_start()
        elif self._check_close():
            # Client has requested to close the connection
            self.close()
        elif self._check_exit():
            # Client requested to close the server (and client)
            raise ServerCloseError('Close server')
        self._reset_read_state()

    def close(self):
        """
        Close the socket connection
        """
        super().close(self.socket)
