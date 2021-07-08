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
import gc
import os
import logging
import socket
from Settings import Settings
from WebIndexItem import WebIndexItem
from WebIndexLoader import WebIndexLoader
from ClientHandlerThread import ClientHandlerThread


class SearchServerMain:
    PROGRAM_VERSION: float = 1.0

    _LISTEN_BACKLOG: int = 64

    def __init__(self):
        self._perform_basic_initialization()

        self._logger: logging.Logger = Settings.get_logger()

        self._web_index: List[WebIndexItem] = WebIndexLoader(self._logger).load_index()
        self._server_socket: socket.socket = self._create_server_socket()

    def _perform_basic_initialization(self) -> None:
        if Settings.WORKING_DIRECTORY is not None:
            os.makedirs(Settings.WORKING_DIRECTORY, exist_ok=True)

            os.chdir(Settings.WORKING_DIRECTORY)

    def _create_server_socket(self) -> socket.socket:
        try:
            os.remove(Settings.SERVER_SOCKET_PATH)
        except OSError:
            pass

        socket_ = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        socket_.bind(Settings.SERVER_SOCKET_PATH)

        if Settings.SERVER_SOCKET_PERMISSIONS is not None:
            os.chmod(Settings.SERVER_SOCKET_PATH, Settings.SERVER_SOCKET_PERMISSIONS)

        socket_.listen(SearchServerMain._LISTEN_BACKLOG)

        return socket_

    def on_server_start(self) -> None:
        self._logger.info("The server has started; listening on Unix socket \"{}\"...".format(Settings.SERVER_SOCKET_PATH))

    def server_loop(self) -> None:
        while True:
            try:
                client_socket, _ = self._server_socket.accept()
            except KeyboardInterrupt:
                break

            gc.collect()

            client_handler_thread = ClientHandlerThread(self._web_index, client_socket)
            client_handler_thread.start()

    def on_server_exit(self) -> None:
        self._logger.info("The server is exiting...")

        self._server_socket.close()
