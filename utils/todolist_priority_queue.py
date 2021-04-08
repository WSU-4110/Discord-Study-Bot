from models import todolist
from queue import PriorityQueue
import heapq
from collections import Counter


class ToDoListPriorityQueue(PriorityQueue):
    """A derived class of the in-built PriorityQueue used to accommodate ToDoList objects"""

    __instance = None

    def __init__(self):
        super().__init__()
        self.alarm_map = Counter()  # a Counter object used to keep track of all the items to fire at a certain point in time
        self.user_map = {}  # a map used to keep track of all the items for a given user
        ToDoListPriorityQueue.__instance = self  # set the static instance as the current (only) instance

    @staticmethod
    def get_instance():
        """Static function to get an instance of the TimerPriorityQueue"""
        if ToDoListPriorityQueue.__instance is None:
            ToDoListPriorityQueue()  # call init here
        return ToDoListPriorityQueue.__instance  # return the static instance

    def add_task(self, a_item: todolist.ToDoList):
        """Function to add a todolistitem-derived object to the queue"""
        self.alarm_map[a_item.end_time] += 1
        if a_item.userid not in self.user_map.keys():
            self.user_map[a_item.userid] = []
        self.user_map[a_item.userid].append(a_item)
        self.put(a_item)

    def get_all_tasks_to_fire(self):
        """Function to get the all the todolistitem-derived objects that will fire at the end time of the top item"""
        tasks_arr = []
        num_items = self.alarm_map[self.peek().end_time]
        for i in range(num_items):
            a_item = self.get_top_task()
            self.user_map[a_item.userid].remove(a_item)
            self.alarm_map[a_item.end_time] -= 1
            tasks_arr.append(a_item)
        return tasks_arr

    def get_top_task(self):
        """Function to get (retrieve and remove) the top todolistitem-derived object from the queue"""
        top_item = self.get()
        return top_item

    def peek(self):
        """Function to peek (retrieve) the top todolistitem-derived object from the queue"""
        if self.empty():
            pass
        else:
            top_item = self.get()
            self.put(top_item)
            return top_item

    def get_all_tasks(self):
        """Function to get the Counter object to retrieve all the todolistitem-derived objects"""
        return self.alarm_map

    def get_tasks_by_user(self, user_id):
        """Function to get the Counter object to retrieve all the todolistitem-derived objects for a given user"""
        return self.user_map[user_id]

    def remove_item(self, message_id):
        """Function to remove a specific item (given a message_id) from the queue using a brute-force O(N) method where"""
        items_to_reinsert = []
        a_item = None
        while True:
            a_item = self.get()
            if a_item.message_id == message_id:
                self.user_map[a_item.userid].remove(a_item)
                self.alarm_map[a_item.end_time] -= 1
                break
            else:
                items_to_reinsert.append(a_item)
        for item in items_to_reinsert:
            self.put(item)
        return a_item

    def __len__(self):
        """Function to get the size of this queue"""
        return self.qsize()
