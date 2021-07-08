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
import logging
import csv
import json
from Settings import Settings
from WebIndexItem import WebIndexItem


class WebIndexLoader:
    def __init__(self, logger: logging.Logger):
        self._logger: logging.Logger = logger

    def load_index(self) -> List[WebIndexItem]:
        self._logger.debug("Loading the web index from \"{}\"...".format(Settings.WEB_INDEX_FILE_PATH))
        web_index_items = self._load_index_from_file()
        self._logger.debug("The web index was loaded successfully! ({} items)".format(len(web_index_items)))

        return web_index_items

    def _load_index_from_file(self) -> List[WebIndexItem]:
        web_index_items = []

        with open(Settings.WEB_INDEX_FILE_PATH) as file:
            reader = csv.reader(file)
            for csv_line in reader:
                parsed_web_index_item = self._parse_index_csv_line(csv_line)
                web_index_items.append(parsed_web_index_item)

        return web_index_items

    def _parse_index_csv_line(self, csv_line: List[str]) -> WebIndexItem:
        parsed_json = json.loads(csv_line[0])

        return WebIndexItem(parsed_json)
