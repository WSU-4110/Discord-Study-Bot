import asyncio
import datetime as dt
from utils import config


async def handle_timers():
    """Asynchronous function that will handle all of the timer-derived objects in the priority queue"""
    while True:  # infinite loop
        top_timer = config.timer_pqueue.peek()  # peek the top timer object from the queue
        print(top_timer.time_remaining())
        if dt.datetime.utcnow() >= top_timer.end_time:  # check if the UTC time now is >= the UTC end time for the top timer
            timers_to_fire = config.timer_pqueue.get_all_tasks_to_fire()  # get all of the timers that need to fire now
            for timer in timers_to_fire:
                await timer.discord_message.channel.send(timer.formatted_discord_message())  # send the discord message for each timer
        await asyncio.sleep(10)  # sleep for 10 seconds and check again
        if len(config.timer_pqueue) == 0:
            break  # temporary behavior
