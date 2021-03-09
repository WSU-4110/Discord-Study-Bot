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
        await ctx.send(f"Note created at {singular_note.time_stamp}!")  # prints to screen

    @commands.command(name="list-notes", aliases=["ln"])  # command to list notes
    async def list_notes(self, ctx):
        userid = ctx.message.author.id  # user ID used as key in dictionary
        i = 1
        for singular_note in cfg.note_dict[userid]:  # looks for user ID in dictionary
            await ctx.send(f"{i} | {singular_note}")  # prints notes to screen
            i += 1

    @commands.command(name="delete-note", aliases=["dn"])  # command to delete note
    async def delete_note(self, ctx, index):
        userid = ctx.message.author.id
        if int(index) <= len(cfg.note_dict[userid]):
            singular_note = cfg.note_dict[userid][(int(index) - 1)]
            singular_note.delete(singular_note.get_message_id())
            del cfg.note_dict[userid][(int(index) - 1)]
            await ctx.send("Note deleted!")


@commands.command(name="embed", aliases=["eb"])
async def embed(self, ctx):
    embed = discord.Embed(title="Sample Embed",
                          url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different "
                                      "components",
                          color=0xFF5733)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(NotesCommands(bot))
