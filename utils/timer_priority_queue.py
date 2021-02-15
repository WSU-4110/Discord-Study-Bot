from utils import timer
from queue import PriorityQueue
import heapq
from collections import Counter


class TimerPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.alarm_map = Counter()

    def add_task(self, a_time: timer.Timer):
        self.alarm_map[a_time.end_time] += 1
        self.put(a_time)

    def get_task(self):
        top_item = self.get()
        return top_item

    def peek(self, reinsert=True):
        if self.empty():
            pass
        else:
            top_item = self.get()
            if reinsert:
                self.put(top_item)
            return top_item


'''
pq = TimerPriorityQueue()
t = timer.Timer('12345', 5, 'Hello')
t2 = timer.Timer('23456', 1, 'Hello 2')
pq.add_task(t)
pq.add_task(t2)
for i in range(10):
    print(pq.peek())
'''
