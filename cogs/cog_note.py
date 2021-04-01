import discord
from discord.ext import commands
from utils import config as cfg
from models import note
from builders.notebuilder import PreBuiltNote
from builders.notedirector import NoteDirector


class NotesCommands(commands.Cog, name="Notes Commands"):
    """These are the notes commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***
    @commands.command(name="create-note", aliases=["cn"])  # command to create a note
    async def create_note(self, ctx, *, msg):
        userid = ctx.message.author.id  # retrieving userid to be used as key in dictionary
        msg_id = ctx.message.id

        # Creating a builder object, passes it to the director and then initiates the construction process
        director = NoteDirector()
        builder = PreBuiltNote
        director.builder = builder
        director.build_note()
        note_object = builder.get_data()  # The end result is retrieved from the builder object

        singular_note = note.Note(msg_id, userid, msg)  # Note object created using message entered by user
        cfg.note_dict[userid].append(singular_note)  # message stored dictionary using user ID
        singular_note.insert(['_message_id', '_userid', '_data', '_time_stamp'])

        embed = discord.Embed(title="Note Created!",
                              description=msg,
                              color=cfg.colors.SUCCESS)
        embed.set_footer(text=f"created at {singular_note.time_stamp}")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(NotesCommands(bot))
