from collections import defaultdict as dd, namedtuple as nt
from typing import *

note_dict = dd(list)

ticket_channel_dict = {}
server_ticket_ctgs = {}

author_ids = [189533543993442304,
              154752622262353921,
              667203504196026422,
              359496559773351936,
              487272627006734339,
              831306913819394068,
              832074432700219422]


def hex_to_int(colhex: str) -> int:
    inthex = int(colhex.replace('#', ''), 16)
    intcol = int(hex(inthex), 0)

    return intcol


class Colors(NamedTuple):
    WSU_GREEN: int  # general info
    WSU_GOLD: int  # user prompts
    SUCCESS: int
    ERROR: int  # input errors
    TIMEOUT: int  # input timeout
    LINK: int  # link color


colors = Colors(
    WSU_GREEN=0x007E6E,
    WSU_GOLD=0XFFD441,
    ERROR=0xFF0000,
    SUCCESS=0x00FF85,
    TIMEOUT=0xFF8500,
    LINK=0x02AAF2
)
