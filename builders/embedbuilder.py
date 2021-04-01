from abc import ABC
import discord
from utils import config as cfg


class EmbedBuilder(ABC):
    def __init__(self):
        self._embed = discord.Embed()

    @property
    def embed(self):
        return self._embed

    def build_title(self):
        ...

    def build_description(self):
        ...

    def build_colour(self):
        ...


class SuccessEmbedBuilder(EmbedBuilder):
    def build_title(self):
        self.embed.title = "Success!"

    def build_description(self):
        self.embed.description = "Command executed successfully."

    def build_colour(self):
        self.embed.colour = cfg.colors.SUCCESS


class ErrorEmbedBuilder(EmbedBuilder):
    def build_title(self):
        self.embed.title = "Error!"

    def build_description(self):
        self.embed.description = "Command failed."

    def build_colour(self):
        self.embed.colour = cfg.colors.ERROR


class TimeoutEmbedBuilder(EmbedBuilder):
    def build_title(self):
        self.embed.title = "Canceled!"

    def build_description(self):
        self.embed.description = "Timed out while waiting for input."

    def build_colour(self):
        self.embed.colour = cfg.colors.TIMEOUT
