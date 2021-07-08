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


from typing import Dict, Any
import re
from CloseConnectionException import CloseConnectionException


class ClientRequest:
    MESSAGE_CLASS: int = 1

    def __init__(self, request_object: Dict[str, Any]):
        if ("search_query" not in request_object) or not isinstance(request_object["search_query"], str):
            raise CloseConnectionException("There is no search query string in the request!")

        if ("max_results" not in request_object) or not isinstance(request_object["max_results"], int):
            raise CloseConnectionException("There is no max results integer in the request!")

        if request_object["max_results"] <= 0:
            raise CloseConnectionException("The max results integer isn't a positive number!")

        if ("use_quotient_based_scoring" not in request_object) or not isinstance(request_object["use_quotient_based_scoring"], bool):
            raise CloseConnectionException("There is no percentile-based ranking boolean in the request!")

        self.canonical_search_query: str = self._canonicalize_query(request_object["search_query"])
        self.max_results: int = request_object["max_results"]
        self.use_quotient_based_scoring: bool = request_object["use_quotient_based_scoring"]

    def _canonicalize_query(self, query: str) -> str:
        query = query.lower()
        query = re.sub(r'\s+', ' ', query)
        query = query.strip()

        return query
