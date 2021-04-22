from collections import defaultdict as dd


class MusicQueue:
    __instance = None

    def __init__(self):
        self.items = dd(list)  # dict (key = server id, val is list)
        MusicQueue.__instance = self

    @staticmethod
    def get_instance():
        """Static function to get an instance of the MusicStack"""
        if MusicQueue.__instance is None:
            MusicQueue()  # call init here
        return MusicQueue.__instance  # return the static instance

    def add_url(self, url: str, server_id: int):
        self.items[server_id].append(url)

    def get_top(self, server_id: int) -> str:
        if self.items[server_id]:
            return self.items[server_id].pop(0)

    def clear_for(self, server_id):
        del self.items[server_id]