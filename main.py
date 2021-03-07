import os
import datetime as dt
from models import timer
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
			if dt.datetime.utcnow() <= end_time:
				orig_channel = bot.get_channel(channel_id)
				orig_message = await orig_channel.fetch_message(message_id)
				print(orig_channel, orig_message)
				config.timer_pqueue.add_task(timer.Timer(user_id, 0, msg, orig_message, start_time=start_time, end_time=end_time))
		except:
			pass


@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await reinit_queue()
    await async_tasks.handle_timers()

	
extensions = [
	'cogs.cog_example',  # Same name as it would be if you were importing it
	'cogs.cog_note',
	'cogs.cog_reminder',
	'cogs.cog_timer',
    	'cogs.cog_search'
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot
