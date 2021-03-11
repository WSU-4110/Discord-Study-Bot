import os
import datetime as dt
from models import timer, reminder, note
from keep_alive import keep_alive
from discord.ext import commands
from utils import database_utils, async_tasks, config

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)


async def reinit_queue():
    timers = database_utils.exec("SELECT * FROM TIMERS")
    for t in timers:
        try:
            message_id, user_id, channel_id, start_time, end_time, msg = t
            if dt.datetime.now() <= end_time:
                orig_channel = bot.get_channel(channel_id)
                orig_message = await orig_channel.fetch_message(message_id)
                config.timer_pqueue.add_task(
                    timer.Timer(user_id, 0, msg, orig_message, start_time=start_time, end_time=end_time))
        except:
            pass

    reminders = database_utils.exec("SELECT * FROM REMINDERS")
    for r in reminders:
        try:
            message_id, user_id, channel_id, start_time, end_time, msg, recurrence = r
            if dt.datetime.now() <= end_time:
                orig_channel = bot.get_channel(channel_id)
                orig_message = await orig_channel.fetch_message(message_id)
                content = orig_message.content.split(' ')
                rem = reminder.Reminder(user_id, msg, orig_message, content[1], int(content[2]), int(content[3]),
                                        recurrence)
                config.timer_pqueue.add_task(rem)
        except:
            pass

    notes = database_utils.exec("SELECT * FROM NOTES")
    for n in notes:
        try:
            message_id, user_id, message, time_stamp = n
            singular_note = note.Note(message_id, user_id, message, time_stamp)
            config.note_dict[int(user_id)].append(singular_note)
        except Exception as e:
            pass


@bot.event
async def on_ready():  # When the bot is ready
    print("collecting information from database")
    await reinit_queue()
    print("starting async tasks")
    print("I'm in and Ready!")
    print(bot.user)  # Prints the bot's username and identifier
    await async_tasks.handle_timers()


extensions = [
    'cogs.cog_example',  # Same name as it would be if you were importing it
    'cogs.cog_note',
    'cogs.cog_reminder',
    'cogs.cog_timer',
    'cogs.cog_search',
    'cogs.cog_profile',
    'cogs.cog_ticket'
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
