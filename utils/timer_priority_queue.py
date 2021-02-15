import timer
from queue import PriorityQueue
import heapq
from collections import Counter


class TimerPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.alarm_map = Counter()

    def add_task(self, a_time: timer.Timer):
        self.alarm_map[a_time.end_time] += 1

    def peek(self):
        if not self.empty():
            pass
        else:
            return None


pq = TimerPriorityQueue()
t = timer.Timer('12345', 1, 'Hello')
t2 = timer.Timer('23456', 5, 'Hello 2')
pq.put(t)
pq.put(t2)
for i in range(10):
    print(pq.get())
