# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from typing import List
import socket
import threading
from WebIndexItem import WebIndexItem
from ClientRequest import ClientRequest
from ClientResponse import ClientResponse
from SearchPerformer import SearchPerformer
from CloseConnectionException import CloseConnectionException
from msgess.msgess import MsgESS


class ClientHandlerThread(threading.Thread):
    def __init__(self, web_index: List[WebIndexItem], client_socket: socket.socket):
        super().__init__(daemon=True)

        self._web_index: List[WebIndexItem] = web_index
        self._client_socket: socket.socket = client_socket

    def run(self) -> None:
        try:
            self._handle_client()

        except (MsgESS.MsgESSException, CloseConnectionException):
            pass

        finally:
            try:
                self._client_socket.close()
            except OSError:
                pass

    def _handle_client(self) -> None:
        client_msgess = MsgESS(self._client_socket)
        client_msgess.set_compress_messages(False)

        request = self._receive_request(client_msgess)
        response = self._handle_request(request)
        self._send_response(client_msgess, response)

    def _receive_request(self, client_msgess: MsgESS) -> ClientRequest:
        json_, message_class = client_msgess.receive_json_object()

        if message_class != ClientRequest.MESSAGE_CLASS:
            raise CloseConnectionException("The client sent a message with an invalid message class. ({})".format(message_class))

        return ClientRequest(json_)

    def _handle_request(self, request: ClientRequest) -> ClientResponse:
        search_results = SearchPerformer(self._web_index, request).perform_search()

        return ClientResponse(search_results)

    def _send_response(self, client_msgess: MsgESS, response: ClientResponse) -> None:
        response_json_object = response.to_json_object()

        client_msgess.send_json_object(response_json_object, ClientResponse.MESSAGE_CLASS)
