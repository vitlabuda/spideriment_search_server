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


from __future__ import annotations
from typing import List, Dict, Any
import re
from SpiderimentSearchServerRuntimeError import SpiderimentSearchServerRuntimeError


class WebIndexItem:
    _HEADING_LEVEL_PARSER_REGEX: re.Pattern = re.compile(r'^h([1-6])$')

    class PageHeading:
        def __init__(self, level: int, text_lc: str):
            self.level: int = level
            self.text_lc: str = text_lc

    def __init__(self, parsed_json: Dict[str, Any]):
        self.url: str = str(parsed_json["final_url"])

        # Converting the string metadata to lowercase makes the search faster, because they are already canonicalized.
        # However, it's not possible to lowercase the items, that are copied to the search result which is then sent to the client (the client should receive the original text).
        self.title: str = str(parsed_json["title"])
        self.headings_lc: List[WebIndexItem.PageHeading] = self._parse_headings(parsed_json["headings"])
        self.description_lc: str = str(parsed_json["description"]).lower()
        self.keywords_lc: str = str(parsed_json["keywords"]).lower()
        self.author_lc: str = str(parsed_json["author"]).lower()

        self.content_snippet: str = str(parsed_json["content_snippet"])
        self.content_snippet_quality: float = float(parsed_json["content_snippet_quality"])
        self.image_alts_lc: str = str(parsed_json["image_alts"]).lower()
        self.link_texts_lc: str = str(parsed_json["link_texts"]).lower()

    def _parse_headings(self, headings_json: Dict[str, List[str]]) -> List[WebIndexItem.PageHeading]:
        headings = []

        for level_str, level_headings in headings_json.items():
            level = WebIndexItem._HEADING_LEVEL_PARSER_REGEX.match(level_str)
            if not level:
                raise SpiderimentSearchServerRuntimeError("A page heading's level is saved incorrectly in the web index! ({})".format(level_str))
            level = int(level[1])

            for text in level_headings:
                heading = WebIndexItem.PageHeading(level, str(text).lower())
                headings.append(heading)

        return headings
