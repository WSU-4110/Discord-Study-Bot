from utils import timer
from queue import PriorityQueue
import heapq
from collections import Counter


class TimerPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.alarm_map = Counter()
        self.user_map = {}

    def add_task(self, a_time: timer.Timer):
        self.alarm_map[a_time.end_time] += 1
        if a_time.userid not in self.user_map.keys():
            self.user_map[a_time.userid] = []
        self.user_map[a_time.userid].append(a_time)
        self.put(a_time)

    def get_all_tasks_to_fire(self):
        tasks_arr = []
        num_items = self.alarm_map[self.peek().end_time]
        for i in range(num_items):
            tasks_arr.append(self.get_top_task())
        return tasks_arr

    def get_top_task(self):
        top_item = self.get()
        return top_item

    def peek(self):
        if self.empty():
            pass
        else:
            top_item = self.get()
            self.put(top_item)
            return top_item

    def get_all_tasks(self):
        return self.alarm_map

    def get_tasks_by_user(self, user_id):
        return self.user_map[user_id]

    def __len__(self):
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
