"""Phillipa the Dolphin Discord Bot."""
import logging
from typing import List

from discord import Client, Message, Reaction, User

from phillipa.emoji import ANGRY, FLOWER, MENTION_EMOJI

LOGGER = logging.getLogger(__name__)


class PhillipaBot(Client):
    """
    Phillipa Discord Client.

    Receives events over websocket protocol and does stuff in response.
    """

    def __init__(self, good_keywords: List[str], bad_keywords: List[str]):
        super().__init__()

        self.good_keywords = good_keywords
        self.bad_keywords = bad_keywords

    async def on_ready(self) -> None:
        """Called when bot is connected."""
        LOGGER.info(f"Connected as {self.user}")

    async def on_message(self, message: Message) -> None:
        """Message received."""
        content = message.content.lower()

        good_conditions = []

        for word in self.good_keywords:
            good_conditions.append(word in content)

        bad_conditions = []

        for word in self.bad_keywords:
            bad_conditions.append(word in content)

        if any(good_conditions) and not any(bad_conditions):
            LOGGER.info("I like")
            await message.add_reaction(FLOWER)

        if self.user in message.mentions and not any(bad_conditions):
            LOGGER.info("I like")
            await message.add_reaction(MENTION_EMOJI)

        if any(bad_conditions):
            LOGGER.info("I dislike")
            await message.add_reaction(ANGRY)

    async def on_reaction_add(self, reaction: Reaction, user: User) -> None:
        """Reaction added to message in cache."""
        if not user.bot and reaction.emoji == FLOWER:
            LOGGER.info(f"{user} is nice.")
            await user.send(FLOWER)
