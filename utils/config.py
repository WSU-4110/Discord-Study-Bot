from utils import timer_priority_queue
from collections import defaultdict as dd
from typing import *

timer_pqueue = timer_priority_queue.TimerPriorityQueue()
note_dict = dd(list)
author_ids = [189533543993442304,
              154752622262353921,
              667203504196026422,
              359496559773351936,
              487272627006734339]


def hex_to_int(colhex: str) -> int:
    inthex = int(colhex.replace('#', ''), 16)
    intcol = int(hex(inthex), 0)

    return intcol
