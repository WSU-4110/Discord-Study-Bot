import discord
from builders import embedbuilder


class EmbedDirector:
    @staticmethod
    def generate_embed(embed_builder: embedbuilder.EmbedBuilder) -> discord.Embed:
        embed_builder.build_title()
        embed_builder.build_description()
        embed_builder.build_colour()
        return embed_builder.embed
