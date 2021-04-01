from duckpy import Client
from models import base_db_model


class Search(base_db_model.BaseDBModel):
    __instance = None

    def __init__(self):
        if Search.__instance is not None:  # singleton should never be re-instantiated
            raise Exception("This class is a singleton!")
        else:
            Search.__instance = self  # generate instance

        self._client = Client()
        self._search_str = None
        self._search_limit = 5
        self._results = None

    def __repr__(self):
        return "**Title:** " + self._result['title'] + \
               "\n**Description:** " + self._result['description'] + \
               "\n" + self._result['url']

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Search.__instance is None:
            Search()
        return Search.__instance

    def set_search_string(self, new_search_str):
        """ _search_str setter """
        self._search_str = new_search_str

    def set_search_limit(self, new_search_limit: int = 5):
        """ _search_limit setter """
        self._search_limit = new_search_limit

    def __get_results_helper(self):
        """ returns duckpy search objects in a size limited list """
        searches = self._client.search(self._search_str)
        results = []

        for i in range(self._search_limit):
            results.append(searches[i])

        return results

    def get_results(self):
        """ returns search results """
        self._results = self.__get_results_helper()
        return self._results

    def get_search_string(self):
        """ _search_str getter """
        return self._search_str

    def get_search_limit(self):
        """ _search_limit getter """
        return self._search_limit
