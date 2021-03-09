from duckpy import Client


class Search:
    def __init__(self, search_str: str, limit_results: int = 5):
        self._client = Client()
        self._search_str = search_str

        if limit_results > 15:
            limit_results = 15
        self._search_limit = limit_results

        self._results = self.__get_results_helper()

    def __repr__(self):
        return "**Title:** " + self._result['title'] + \
               "\n**Description:** " + self._result['description'] + \
               "\n" + self._result['url']

    def __get_results_helper(self):
        searches = self._client.search(self._search_str)
        results = []

        for i in range(self._search_limit):
            results.append(searches[i])

        return results

    def get_results(self):
        return self._results

    def get_search_string(self):
        return self._search_str

    def get_search_limit(self):
        return self._search_limit