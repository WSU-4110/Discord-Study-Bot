from utils import timer_priority_queue
from collections import defaultdict as dd, namedtuple as nt
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


class Colors(NamedTuple):
    WSU_GREEN: int  # general info
    WSU_GOLD: int  # user prompts
    ERROR: int  # input errors
    TIMEOUT: int  # input timeout


colors = Colors(
    WSU_GREEN=0x00584D,
    WSU_GOLD=0XFFC842,
    ERROR=0xFF0000,
    TIMEOUT=0x777777
)
