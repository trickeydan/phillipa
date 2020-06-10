"""Phillipa the Dolphin Discord Bot."""
import logging
import re
from typing import List, Pattern

from discord import Activity, ActivityType, Client, Message, Reaction, User

from phillipa.emoji import ANGRY, FLOWER
from phillipa.trigger import (
    MessageRegexReactTrigger,
    Trigger,
    UserMentionedReactTrigger,
)

LOGGER = logging.getLogger(__name__)


class PhillipaBot(Client):
    """
    Phillipa Discord Client.

    Receives events over websocket protocol and does stuff in response.
    """

    def __init__(self, good_keywords: List[str], bad_keywords: List[str]):
        super().__init__()
        good_patterns: List[Pattern[str]] = [
            re.compile(kw, flags=re.IGNORECASE) for kw in good_keywords
        ]
        bad_patterns: List[Pattern[str]] = [
            re.compile(kw, flags=re.IGNORECASE) for kw in bad_keywords
        ]

        self.triggers: List[Trigger] = [
            MessageRegexReactTrigger(bad_patterns, ANGRY),
            MessageRegexReactTrigger(good_patterns, FLOWER),
        ]

    async def on_ready(self) -> None:
        """Called when bot is connected."""
        LOGGER.info(f"Connected as {self.user}")
        await self.change_presence(
            activity=Activity(type=ActivityType.playing, name="in the waves"),
        )

        self.triggers.append(UserMentionedReactTrigger(self.user, FLOWER))

    async def on_message(self, message: Message) -> None:
        """Message received."""
        for trigger in self.triggers:
            result = await trigger.try_message(message)
            if result:
                return

    async def on_reaction_add(self, reaction: Reaction, user: User) -> None:
        """Reaction added to message in cache."""
        if not user.bot and reaction.emoji == FLOWER:
            LOGGER.info(f"{user} is nice.")
            await user.send(FLOWER)
