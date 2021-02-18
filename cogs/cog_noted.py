import discord
from discord.ext import commands
from utils import notes, config as cfg


class NotesCommands(commands.Cog, name="Notes Commands"):
    """These are the notes commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***

    @commands.command(name="create-note", aliases=["cn"])
    async def create_note(self, ctx, *msg: str):
        userid = ctx.message.author.id
        note = notes.Note(userid, ' '.join(msg))
        cfg.note_dict[userid].append(note)
        await ctx.send(f"Note created at {note.time_stamp}!")

    @commands.command(name="list-notes", aliases=["ln"])
    async def list_notes(self, ctx):
        userid = ctx.message.author.id
        for note in cfg.note_dict[userid]:
            message = await ctx.send(f"{note}")
            #await message.add_reaction("❌")

    # *** commands end above ***

    # feature in progress
    #@commands.Cog.listener()
    #async def on_reaction_add(self, reaction, user):
    #    channel = reaction.message.channel
    #    await channel.send(f"reaction detected by {user}.\n{reaction.message}")

def setup(bot):
    bot.add_cog(NotesCommands(bot))
