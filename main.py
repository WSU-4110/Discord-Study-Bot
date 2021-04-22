import os
import datetime as dt
import discord
from models import timer, reminder, note, ticket
from factories.embedfactory import EmbedFactory
from keep_alive import keep_alive
from discord.ext import commands
from utils import database_utils, async_tasks, config, timer_priority_queue
# from dotenv import load_dotenv

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=discord.Intents.all()
)


async def reinit_queue():
    timers = database_utils.exec("SELECT * FROM TIMERS")
    for t in timers:
        try:
            message_id, user_id, channel_id, start_time, end_time, msg = t
            if dt.datetime.now() <= end_time:
                orig_channel = bot.get_channel(channel_id)
                orig_message = await orig_channel.fetch_message(message_id)
                timer_priority_queue.TimerPriorityQueue.get_instance().add_task(
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
                timer_priority_queue.TimerPriorityQueue.get_instance().add_task(rem)
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

    tickets = database_utils.exec("SELECT * FROM TICKETS")
    for message_id, user_id, channel_id, question, roles in tickets:
        try:
            ticket_obj = ticket.Ticket(message_id, user_id, channel_id, question, roles)
            config.ticket_channels[channel_id] = ticket_obj
        except Exception as e:
            pass

    ticket_categories = database_utils.exec("SELECT * FROM SERVER_TICKET_CATEGORIES")
    for server_id, ctg_id in ticket_categories:
        config.server_ticket_ctgs[server_id] = ctg_id

    user_tz_info = database_utils.exec("SELECT * FROM USER_INFO")
    for user_id, tz, score in user_tz_info:
        config.user_tzs[user_id] = tz


@bot.event
async def on_ready():  # When the bot is ready
    print("collecting information from database")
    await reinit_queue()
    print("starting async tasks")
    print("I'm in and Ready!")
    print(bot.user)  # Prints the bot's username and identifier
    await async_tasks.run_tasks()


extensions = [
    'cogs.cog_example',  # Same name as it would be if you were importing it
    'cogs.cog_note',
    'cogs.cog_reminder',
    'cogs.cog_timer',
    'cogs.cog_search',
    'cogs.cog_profile',
    'cogs.cog_ticket',
    'cogs.cog_todolist',
    'cogs.cog_easteregg',
    'cogs.cog_music'
]


@bot.event
async def on_command_error(ctx, error):
    await EmbedFactory.error(ctx, f'Error! `{error}`')


if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
# load_dotenv()
# token = os.getenv("DISCORD_BOT_SECRET")
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
