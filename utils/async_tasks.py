import asyncio
import datetime as dt
import os

from utils import config, timer_priority_queue, todolist_priority_queue, music_queue
import discord
from cogs import cog_music


async def run_tasks(bot):
    while True:
        if len(timer_priority_queue.TimerPriorityQueue.get_instance()) == 0:
            pass
        else:
            await handle_timers()

        if len(todolist_priority_queue.ToDoListPriorityQueue.get_instance()) == 0:
            pass
        else:
            await handle_todolists()
        await check_music_status(bot)
        await asyncio.sleep(3)  # sleep for 3 seconds and check again


async def handle_timers():
    """Asynchronous function that will handle all of the timer-derived objects in the priority queue"""
    top_timer = timer_priority_queue.TimerPriorityQueue.get_instance().peek()  # peek the top timer object from the queue
    print(top_timer.time_remaining())
    if dt.datetime.utcnow() >= top_timer.end_time:  # check if the UTC time now is >= the UTC end time for the top timer
        timers_to_fire = timer_priority_queue.TimerPriorityQueue.get_instance().get_all_tasks_to_fire()  # get all of the timers that need to fire now
        for timer in timers_to_fire:
            if timer.pre_flight_for_deletion():
                timer.delete(timer.message_id)
            print(timer.discord_message.channel)
            if timer.discord_message.channel.type is discord.ChannelType.private:
                await timer.discord_message.author.send(timer.formatted_discord_message(),
                                                        embed=timer.embed())  # send the discord message for each timer
            else:
                try:
                    server = timer.discord_message.guild
                    for role_id in timer.roles.split(' '):
                        for member in server.members:
                            if role_id in [role.mention for role in member.roles]:
                                await member.send(embed=timer.embed())  # send the discord message for each user in the role
                except Exception as e:
                    print(e)
                    try:  # fallback to sending to the author
                        await timer.discord_message.author.send(timer.formatted_discord_message(), embed=timer.embed())  # send the discord message for each timer
                    except:
                        pass  # multiple points of error lmao



async def handle_todolists():
    """Asynchronous function that will handle all of the todolistitem-derived objects in the priority queue"""
    top_item = todolist_priority_queue.ToDoListPriorityQueue.get_instance().peek()  # peek the top item object from the queue
    print(top_item.time_remaining())
    if dt.datetime.utcnow() >= top_item.end_time:  # check if the UTC time now is >= the UTC end time for the top item
        items_to_fire = todolist_priority_queue.ToDoListPriorityQueue.get_instance().get_all_tasks_to_fire()  # get all of the items that need to fire now
        for item in items_to_fire:
            '''
            if item.pre_flight_for_deletion():
                item.delete(item.message_id)
            '''
            await item.discord_message.author.send(item.formatted_discord_message() + ' of ' + repr(item))  # send the discord message for each item


async def check_music_status(bot):
    for guild_id, status in config.server_playing_music.items():
        if status:
            guild = bot.get_guild(guild_id)
            voice = discord.utils.get(bot.voice_clients, guild=guild)
            if not voice.is_playing() and len(music_queue.MusicQueue.get_instance().items[guild_id]) > 0:
                config.server_playing_music[guild_id] = False
                song_tuple = music_queue.MusicQueue.get_instance().get_top(guild_id)
                await bot.get_cog("Music Commands").play_next_song(song_tuple[1], song_tuple[0])
