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

        good: bool = self._message_matches(self.good_keywords, message)
        bad: bool = self._message_matches(self.bad_keywords, message)

        if bad:
            LOGGER.info("I dislike")
            await message.add_reaction(ANGRY)
        else:
            if good or self.user in message.mentions:
                LOGGER.info("I like")
                await message.add_reaction(FLOWER)            

    async def on_reaction_add(self, reaction: Reaction, user: User) -> None:
        """Reaction added to message in cache."""
        if not user.bot and reaction.emoji == FLOWER:
            LOGGER.info(f"{user} is nice.")
            await user.send(FLOWER)

    def _message_matches(self, pattern_list: List[str], message: Message) -> bool:
        """Check if the message matches any of the patterns."""
        content = message.content.lower()
        return any([self._message_compare(pattern, content) for pattern in pattern_list])


    def _message_compare(self, pattern: str, content: str) -> bool:
        """Comparison function."""
        return pattern in content