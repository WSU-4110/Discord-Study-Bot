import asyncio
import discord
from discord.ext import commands
from utils import config as cfg
from models import note


class NotesCommands(commands.Cog, name="Notes Commands"):
    """These are the notes commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***
    @commands.command(name="create-note", aliases=["cn"])  # command to create a note
    async def create_note(self, ctx, *, msg):
        userid = ctx.message.author.id  # retrieving userid to be used as key in dictionary
        msg_id = ctx.message.id
        singular_note = note.Note(msg_id, userid, msg)  # Note object created using message entered by user
        cfg.note_dict[userid].append(singular_note)  # message stored dictionary using user ID
        singular_note.insert(['_message_id', '_userid', '_data', '_time_stamp'])

        embed = discord.Embed(title="Note Created!",
                              description=msg,
                              color=cfg.colors.SUCCESS)
        embed.set_footer(text=f"created at {singular_note.time_stamp}")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="list-notes", aliases=["ln"])  # command to list notes
    async def list_notes(self, ctx):
        """ list notes """
        userid = ctx.message.author.id  # user ID used as key in dictionary
        i = 1
        embed = discord.Embed(title=f"Notes",
                              color=cfg.colors.WSU_GREEN)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        for singular_note in cfg.note_dict[userid]:  # looks for user ID in dictionary
            embed.add_field(name=f"Note {i}",
                            value="created on: " + str(singular_note.time_stamp) +
                                   "\nNote: " + str(singular_note.get_data()),
                            inline=False)
            i += 1
        await ctx.send(embed=embed)  # prints notes to screen

    @commands.command(name="delete-note", aliases=["dn"])  # command to delete note
    async def delete_note(self, ctx):
        """ Delete user notes """
        await self.list_notes(ctx)
        try:
            # asks user for what they want to search for
            embed = discord.Embed(title="which note do you want to delete?",
                                  description="example: 3",
                                  color=cfg.colors.WSU_GOLD)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            index = await self.bot.wait_for('message',
                                            timeout=60.0,
                                            check=lambda message: message.author == ctx.author)
            index = index.content

            # deletion process starts
            userid = ctx.message.author.id
            if int(index) <= len(cfg.note_dict[userid]):
                # delete note from memory and database
                singular_note = cfg.note_dict[userid][(int(index) - 1)]
                singular_note.delete(singular_note.get_message_id())
                del cfg.note_dict[userid][(int(index) - 1)]

                # output to user
                embed = discord.Embed(title="Note Deleted!",
                                      color=cfg.colors.SUCCESS)
                embed.set_footer(text=f"created at {singular_note.time_stamp}")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                # index out of range error handling
                embed = discord.Embed(title="Index out of range!",
                                      color=cfg.colors.ERROR,
                                      description="Make sure to type in the number in the title of the note.")
                embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            # in case user takes more than 60 seconds to respond, send message
            embed = discord.Embed(title="Timeout Error!!!",
                                  description="took more than 60 seconds to respond.",
                                  color=cfg.colors.TIMEOUT)
            embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
            await ctx.send(embed=embed)
        except ValueError:
            # in case user takes more than 60 seconds to respond, send message
            embed = discord.Embed(title="Invalid input!!!",
                                  description="please enter a number such as '6' or '21'.",
                                  color=cfg.colors.ERROR)
            embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(NotesCommands(bot))
