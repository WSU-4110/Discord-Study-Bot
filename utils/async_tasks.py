import asyncio
from utils import config


async def handle_timers():
    while True:
        top_timer = config.timer_pqueue.peek()
        print(top_timer.time_remaining)
        await asyncio.sleep(10)
        if len(config.timer_pqueue) == 0:
            break
