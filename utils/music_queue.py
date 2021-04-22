from collections import defaultdict as dd
from typing import Tuple


class MusicQueue:
    __instance = None

    def __init__(self):
        self.items = dd(list)  # dict (key = server id, val is list of tuples)
        MusicQueue.__instance = self

    @staticmethod
    def get_instance():
        """Static function to get an instance of the MusicStack"""
        if MusicQueue.__instance is None:
            MusicQueue()  # call init here
        return MusicQueue.__instance  # return the static instance

    def add_url(self, url: str, server_id: int, ctx):
        self.items[server_id].append((url, ctx))

    def get_top(self, server_id: int) -> Tuple:
        if self.items[server_id]:
            return self.items[server_id].pop(0)

    def clear_for(self, server_id):
        del self.items[server_id]