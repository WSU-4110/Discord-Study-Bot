import asyncio
import datetime as dt
from utils import config


async def handle_timers(message_to_send=None):
    while True:
        top_timer = config.timer_pqueue.peek()
        print(top_timer.time_remaining())
        if dt.datetime.now() >= top_timer.end_time:
            timers_to_fire = config.timer_pqueue.get_all_tasks_to_fire()
            for timer in timers_to_fire:
                if message_to_send is None:
                    message_to_send = f"{timer.discord_message.author.mention} Your timer for {str(timer.end_time)} has finished. " \
                                      f"'Here's your initial message: {timer.msg}"
                await timer.discord_message.channel.send(message_to_send)
        await asyncio.sleep(10)
        if len(config.timer_pqueue) == 0:
            break
