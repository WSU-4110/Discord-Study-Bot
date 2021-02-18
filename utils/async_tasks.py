import asyncio
import datetime as dt
from utils import config


async def handle_timers():
    while True:
        top_timer = config.timer_pqueue.peek()
        print(top_timer.time_remaining())
        if dt.datetime.now() >= top_timer.end_time:
            timers_to_fire = config.timer_pqueue.get_all_tasks_to_fire()
            for timer in timers_to_fire:
                await timer.discord_message.channel.send(timer.formatted_discord_message())
        await asyncio.sleep(10)
        if len(config.timer_pqueue) == 0:
            break
