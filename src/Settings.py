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


from typing import Optional
import sys
import logging


class Settings:
    WORKING_DIRECTORY: Optional[str] = "working_dir/"

    WEB_INDEX_FILE_PATH: str = "web_index.csv"

    SERVER_SOCKET_PATH: str = "spideriment_search_server.sock"
    SERVER_SOCKET_PERMISSIONS: Optional[int] = 0o777

    MINIMAL_SCORE: float = 1.0

    # These are the scoring coefficients for the result ranking algorithm.
    SCORE_URL: int = 2000
    SCORE_TITLE: int = 20000
    SCORE_HEADING: int = 5000  # this score will be divided by the heading's level (e.g. h1: 500 / 1 = 500; h2: 500 / 2 = 250; etc.)
    SCORE_DESCRIPTION: int = 1500
    SCORE_KEYWORD: int = 50
    SCORE_AUTHOR: int = 7500
    SCORE_CONTENT_SNIPPET: int = 100  # scoring coefficient * content_snippet_quality
    SCORE_IMAGE_ALT: int = 200
    SCORE_LINK_TEXT: int = 100

    @staticmethod
    def get_logger() -> logging.Logger:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        return logging.getLogger("spideriment_search_server")
