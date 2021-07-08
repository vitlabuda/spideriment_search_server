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


from typing import List, Callable
from Settings import Settings
from WebIndexItem import WebIndexItem
from ClientRequest import ClientRequest
from SearchResult import SearchResult


class SearchPerformer:
    def __init__(self, web_index: List[WebIndexItem], request: ClientRequest):
        self._web_index: List[WebIndexItem] = web_index
        self._request: ClientRequest = request

    def perform_search(self) -> List[SearchResult]:
        search_results = []
        if not self._request.canonical_search_query:
            return search_results  # If the search query is empty, don't return any results

        for web_index_item in self._web_index:
            search_result = self._get_search_result(web_index_item)
            if search_result.score >= Settings.MINIMAL_SCORE:
                search_results.append(search_result)

        search_results.sort(key=lambda item: item.score, reverse=True)

        return search_results[0:self._request.max_results]

    def _get_search_result(self, web_index_item: WebIndexItem) -> SearchResult:
        search_result = SearchResult(web_index_item)

        url_lc = web_index_item.url.lower()
        title_lc = web_index_item.title.lower()
        content_snippet_lc = web_index_item.content_snippet.lower()

        if self._request.use_quotient_based_scoring:
            # --- Percentile-based scoring algorithm ---
            search_result.score += self._zdse(lambda: (url_lc.count(self._request.canonical_search_query) / len(url_lc)) * Settings.SCORE_URL)
            search_result.score += self._zdse(lambda: (title_lc.count(self._request.canonical_search_query) / len(title_lc)) * Settings.SCORE_TITLE)
            for heading in web_index_item.headings_lc:  # functools.reduce() could be used here, but the resulting code is very difficult to read
                search_result.score += self._zdse(lambda: (heading.text_lc.count(self._request.canonical_search_query) / len(heading.text_lc)) * (Settings.SCORE_HEADING / heading.level))
            search_result.score += self._zdse(lambda: (web_index_item.description_lc.count(self._request.canonical_search_query) / len(web_index_item.description_lc)) * Settings.SCORE_DESCRIPTION)
            search_result.score += self._zdse(lambda: (web_index_item.keywords_lc.count(self._request.canonical_search_query) / len(web_index_item.keywords_lc)) * Settings.SCORE_KEYWORD)
            search_result.score += self._zdse(lambda: (web_index_item.author_lc.count(self._request.canonical_search_query) / len(web_index_item.author_lc)) * Settings.SCORE_AUTHOR)
            search_result.score += self._zdse(lambda: (content_snippet_lc.count(self._request.canonical_search_query) / len(content_snippet_lc)) * web_index_item.content_snippet_quality * Settings.SCORE_CONTENT_SNIPPET)
            search_result.score += self._zdse(lambda: (web_index_item.image_alts_lc.count(self._request.canonical_search_query) / len(web_index_item.image_alts_lc)) * Settings.SCORE_IMAGE_ALT)
            search_result.score += self._zdse(lambda: (web_index_item.link_texts_lc.count(self._request.canonical_search_query) / len(web_index_item.link_texts_lc)) * Settings.SCORE_LINK_TEXT)
        else:
            # --- Occurrence-based scoring algorithm ---
            search_result.score += url_lc.count(self._request.canonical_search_query) * Settings.SCORE_URL
            search_result.score += title_lc.count(self._request.canonical_search_query) * Settings.SCORE_TITLE
            for heading in web_index_item.headings_lc:  # functools.reduce() could be used here, but the resulting code is very difficult to read
                search_result.score += heading.text_lc.count(self._request.canonical_search_query) * (Settings.SCORE_HEADING / heading.level)
            search_result.score += web_index_item.description_lc.count(self._request.canonical_search_query) * Settings.SCORE_DESCRIPTION
            search_result.score += web_index_item.keywords_lc.count(self._request.canonical_search_query) * Settings.SCORE_KEYWORD
            search_result.score += web_index_item.author_lc.count(self._request.canonical_search_query) * Settings.SCORE_AUTHOR
            search_result.score += content_snippet_lc.count(self._request.canonical_search_query) * web_index_item.content_snippet_quality * Settings.SCORE_CONTENT_SNIPPET
            search_result.score += web_index_item.image_alts_lc.count(self._request.canonical_search_query) * Settings.SCORE_IMAGE_ALT
            search_result.score += web_index_item.link_texts_lc.count(self._request.canonical_search_query) * Settings.SCORE_LINK_TEXT

        return search_result

    # Zero-division safety ensurer
    def _zdse(self, f: Callable[[], float]) -> float:
        try:
            return f()
        except ZeroDivisionError:
            return 0.0
