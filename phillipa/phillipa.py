"""Phillipa the Dolphin Discord Bot."""
import logging
import re
from typing import List, Pattern

from discord import Activity, ActivityType, Client, Message, Reaction, User

from phillipa.emoji import ANGRY, FLOWER

LOGGER = logging.getLogger(__name__)


class PhillipaBot(Client):
    """
    Phillipa Discord Client.

    Receives events over websocket protocol and does stuff in response.
    """

    def __init__(self, good_keywords: List[str], bad_keywords: List[str]):
        super().__init__()

        self.good_patterns: List[Pattern[str]] = [re.compile(kw, flags=re.IGNORECASE) for kw in good_keywords]
        self.bad_patterns: List[Pattern[str]] = [re.compile(kw, flags=re.IGNORECASE) for kw in bad_keywords]

    async def on_ready(self) -> None:
        """Called when bot is connected."""
        LOGGER.info(f"Connected as {self.user}")
        await self.change_presence(activity=Activity(type=ActivityType.playing, name="in the waves"))

    async def on_message(self, message: Message) -> None:
        """Message received."""
        good: bool = self._message_matches(self.good_patterns, message)
        bad: bool = self._message_matches(self.bad_patterns, message)

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

    def _message_matches(
        self,
        pattern_list: List[Pattern[str]],
        message: Message,
    ) -> bool:
        """Check if the message matches any of the patterns."""
        return any(self._message_compare(pattern, message.content) for pattern in pattern_list)

    def _message_compare(self, pattern: Pattern[str], content: str) -> bool:
        """Comparison function."""
        return re.search(pattern, content) is not None
