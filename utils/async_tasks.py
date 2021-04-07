import asyncio
import datetime as dt
from utils import config, timer_priority_queue
import discord
from models import reminder


async def handle_timers():
    """Asynchronous function that will handle all of the timer-derived objects in the priority queue"""
    while True:  # infinite loop
        if len(timer_priority_queue.TimerPriorityQueue.get_instance()) == 0:
            await asyncio.sleep(5)
            continue  # temporary behavior
        top_timer = timer_priority_queue.TimerPriorityQueue.get_instance().peek()  # peek the top timer object from the queue
        print(top_timer.time_remaining())
        if dt.datetime.utcnow() >= top_timer.end_time:  # check if the UTC time now is >= the UTC end time for the top timer
            timers_to_fire = timer_priority_queue.TimerPriorityQueue.get_instance().get_all_tasks_to_fire()  # get all of the timers that need to fire now
            for timer in timers_to_fire:
                if timer.pre_flight_for_deletion():
                    timer.delete(timer.message_id)
                print(timer.discord_message.channel)
                if timer.discord_message.channel.type is discord.ChannelType.private:
                    await timer.discord_message.author.send(timer.formatted_discord_message(), embed=timer.embed())  # send the discord message for each timer
                else:
                    try:
                        server = timer.discord_message.guild
                        for role_id in timer.roles.split(' '):
                            for member in server.members:
                                if role_id in [role.mention for role in member.roles]:
                                    await member.send(timer.formatted_discord_message(), embed=timer.embed())  # send the discord message for each user in the role
                    except Exception as e:
                        print(e)
        await asyncio.sleep(3)  # sleep for 10 seconds and check again
