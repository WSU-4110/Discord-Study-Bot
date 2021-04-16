import discord
import asyncio
from discord.ext import commands
import random
from utils import config as cfg


class EasterEggCommands(commands.Cog, name="Easter Egg Commands"):
    """These are the easter egg commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8-ball", aliases=["8ball", "8b"])  # command to create a note
    async def eight_ball(self, ctx, *, question: str):
        """ Play magic 8-ball, answers to everything """
        try:
            positive_responses = [
                'It is certain.',
                'It is decidedly so.',
                'Without a doubt',
                'Yes - definetly',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.'
            ]
            hazy_responses = [
                'Reply hazy, try again',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now',
                'Concentrate and ask again.'
            ]
            negative_responses = [
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.'
            ]
            responses = [*positive_responses, *hazy_responses, *negative_responses] # single list of responses
            response = random.choice(responses) # select response

            # determine type of response for embed
            if response in positive_responses:
                colour = cfg.colors.SUCCESS
            elif response in hazy_responses:
                colour = cfg.colors.WSU_GOLD
            elif response in negative_responses:
                colour = cfg.colors.ERROR

            # output embed
            embed = discord.Embed(title="Magic 8-Ball:", color=colour)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/" +
                    "?u=https%3A%2F%2Fwww.bigw.com.au%2Fmedias%2Fsys" +
                    "_master%2Fimages%2Fimages%2Fhd5%2Fh14%2F13660536602654.jpg&f=1&nofb=1")
            embed.add_field(name=response, value="Statement: " + question, inline=True)
            await ctx.send(embed=embed)  # sends output message
        except asyncio.TimeoutError:
            # in case user takes more than 60 seconds to respond, send message
            embed = discord.Embed(title="Timeout Error!!!",
                                  description="took more than 60 seconds to respond.",
                                  color=cfg.colors.TIMEOUT)
            embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
            await ctx.send(embed=embed)

    @commands.command(name="rock-paper-scissors", aliases=["rps"])  # command to create a note
    async def rps(self, ctx):
        try:
            # asks user selection
            emojis = ["🪨", "📜", "✂️"]

            # create embed to ask user choice
            embed = discord.Embed(title="Choose rock paper or scissors!",
                                  description="click the emoji/reactions!",
                                  color=cfg.colors.WSU_GOLD)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.istockphoto.com%2" +
                    "Fphotos%2Frock-paper-scissors-picture-id172245258%3Fk%3D6%26m%3D172245258%26s%3D612x6" +
                    "12%26w%3D0%26h%3DNh1HajvkB5bANhHZ6Ny9w9tNleYVaBwp7jwnNdEtjPg%3D&f=1&nofb=1")
            msg = await ctx.send(embed=embed)

            for emoji in emojis:  # add emoji to the message
                await msg.add_reaction(emoji)

            # get user input
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     timeout=60.0,
                                                     check=(lambda emj, usr:
                                                            usr == ctx.author
                                                            and emj.message == msg
                                                            and emj.emoji in emojis))

            bot_choice = random.choice(['Rock', 'Paper', 'Scissors'])

            # set emoji and image for bot
            if bot_choice == "Rock":
                emoji = emojis[0]
                img = "https://jooinn.com/images/rock-1.jpg"
            elif bot_choice == "Paper":
                emoji = emojis[1]
                img = "https://i.ytimg.com/vi/hFFpoIv7YKg/maxresdefault.jpg"
            else:
                emoji = emojis[2]
                img = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia." \
                      "istockphoto.com%2Fphotos%2Fopen-scissors-with-red-handle-isolated" \
                      "-on-white-picture-id517231506%3Fk%3D6%26m%3D517231506%26s%3D612x6" \
                      "12%26w%3D0%26h%3DFG8dBeuKmNzA44ee-lFMdKzlLYxGnYcFVTMaIbHvNeE%3D&f=1&nofb=1"

            # win-lose-tie casses
            if (bot_choice == "Rock" and reaction.emoji == emojis[0])\
                    or (bot_choice == "Paper" and reaction.emoji == emojis[1])\
                    or (bot_choice == "Scissors" and reaction.emoji == emojis[2]):  # tied
                color = cfg.colors.LINK
                custom_title = "Tied!"
            elif (bot_choice == "Paper" and reaction.emoji == emojis[0])\
                    or (bot_choice == "Scissors" and reaction.emoji == emojis[1])\
                    or (bot_choice == "Rock" and reaction.emoji == emojis[2]):  # bot wins
                color = cfg.colors.ERROR
                custom_title = "Oh no! you lost."
            else:  # player wins
                color = cfg.colors.SUCCESS
                custom_title = "Yay! you won."

            # output embed
            embed = discord.Embed(title=custom_title,
                                  description=f"Bot: {emoji}\nYou: {reaction.emoji}",
                                  color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url=img)
            msg = await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            # in case user takes more than 60 seconds to respond, send message
            embed = discord.Embed(title="Timeout Error!!!",
                                  description="took more than 60 seconds to respond.",
                                  color=cfg.colors.TIMEOUT)
            embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
            await ctx.send(embed=embed)

    @commands.command(name="guessing-game", aliases=["guess", "gg"])  # command to create a note
    async def guessing_game(self, ctx):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        used_emojis = []
        end_game_flag = True  # manages game loop
        final_message_flag = True  # makes sure eng game message is
        attempt_limit = 5
        attempts = attempt_limit
        secret_answer_emoji = random.choice(emojis)
        custom_title = "Guess the number!"
        description = f"Wait for all emojis to be added before reacting/selecting."
        color = cfg.colors.WSU_GOLD

        # game loop starts
        while end_game_flag or final_message_flag:
            try:
                if not end_game_flag:
                    final_message_flag = False
                # create embed to ask user to guess
                embed = discord.Embed(title=custom_title,
                                      description=description,
                                      color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=embed)

                if final_message_flag:
                    for emoji in emojis:  # add emoji to the message
                        if not (emoji in used_emojis):
                            await msg.add_reaction(emoji)
                    await msg.add_reaction("❌")  # quit button

                    # get user input
                    reaction, user = await self.bot.wait_for('reaction_add',
                                                             timeout=60.0,
                                                             check=(lambda emj, usr:
                                                                    usr == ctx.author
                                                                    and emj.message == msg
                                                                    and (emj.emoji in emojis
                                                                         or emj.emoji == "❌")))

                    used_emojis.append(reaction.emoji)

                    if reaction.emoji == "❌":  # user quits
                        custom_title = "You gave up!"
                        description = f"The answer was {secret_answer_emoji}.\nAttempts left: {attempts}."
                        color = cfg.colors.TIMEOUT
                        end_game_flag = False
                    elif attempts == 1:  # user lost
                        custom_title = "Oh no! you lost."
                        description = f"The answer was {secret_answer_emoji}."
                        color = cfg.colors.ERROR
                        end_game_flag = False
                    elif reaction.emoji == secret_answer_emoji:  # user wins
                        custom_title = "Yay! you won."
                        description = f"you guessed correctly in {attempt_limit - attempts + 1} attempts."
                        color = cfg.colors.SUCCESS
                        end_game_flag = False
                    else:  # user guessed wrong
                        attempts -= 1
                        custom_title = "You guessed wrong! Try again."
                        description = f"Attempts left: {attempts}."
                        color = cfg.colors.WSU_GOLD
            except asyncio.TimeoutError:
                # in case user takes more than 60 seconds to respond, send message
                embed = discord.Embed(title="Timeout Error!!!",
                                      description="took more than 60 seconds to respond.",
                                      color=cfg.colors.TIMEOUT)
                embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
                await ctx.send(embed=embed)
                end_game_flag = False
                final_message_flag = False


def setup(bot):
    bot.add_cog(EasterEggCommands(bot))  # automatically called by load_extension() in 'main.py'
