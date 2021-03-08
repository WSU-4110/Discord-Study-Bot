from models import timer
from queue import PriorityQueue
import heapq
from collections import Counter


class TimerPriorityQueue(PriorityQueue):
    """A derived class of the in-built PriorityQueue used to accommodate Timer objects"""

    def __init__(self):
        super().__init__()
        self.alarm_map = Counter()  # a Counter object used to keep track of all the timers to fire at a certain point in time
        self.user_map = {}  # a map used to keep track of all the timers for a given user

    def add_task(self, a_time: timer.Timer):
        """Function to add a timer-derived object to the queue"""
        self.alarm_map[a_time.end_time] += 1
        if a_time.userid not in self.user_map.keys():
            self.user_map[a_time.userid] = []
        self.user_map[a_time.userid].append(a_time)
        self.put(a_time)

    def get_all_tasks_to_fire(self):
        """Function to get the all the timer-derived objects that will fire at the end time of the top timer"""
        tasks_arr = []
        num_items = self.alarm_map[self.peek().end_time]
        for i in range(num_items):
            a_time = self.get_top_task()
            self.user_map[a_time.userid].remove(a_time)
            self.alarm_map[a_time.end_time] -= 1
            tasks_arr.append(a_time)
        return tasks_arr

    def get_top_task(self):
        """Function to get (retrieve and remove) the top timer-derived object from the queue"""
        top_item = self.get()
        return top_item

    def peek(self):
        """Function to peek (retrieve) the top timer-derived object from the queue"""
        if self.empty():
            pass
        else:
            top_item = self.get()
            self.put(top_item)
            return top_item

    def get_all_tasks(self):
        """Function to get the Counter object to retrieve all the timer-derived objects"""
        return self.alarm_map

    def get_tasks_by_user(self, user_id):
        """Function to get the Counter object to retrieve all the timer-derived objects for a given user"""
        return self.user_map[user_id]

    def remove_timer(self, message_id):
        """Function to remove a specific timer (given a message_id) from the queue using a brute-force O(N) method where"""
        items_to_reinsert = []
        a_time = None
        while True:
            a_time = self.get()
            if a_time.message_id == message_id:
                self.user_map[a_time.userid].remove(a_time)
                self.alarm_map[a_time.end_time] -= 1
                break
            else:
                items_to_reinsert.append(a_time)
        for item in items_to_reinsert:
            self.put(item)
        return a_time

    def __len__(self):
        """Function to get the size of this queue"""
        return self.qsize()


'''
pq = TimerPriorityQueue()
t = timer.Timer('12345', 5, 'Hello')
t2 = timer.Timer('23456', 1, 'Hello 2')
pq.add_task(t)
pq.add_task(t2)
for i in range(10):
    print(pq.peek())
'''
