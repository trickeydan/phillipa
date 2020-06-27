"""Phillipa the Dolphin Discord Bot."""
import logging
import re
from typing import List, Pattern

from discord import Activity, ActivityType, Client, Message, Reaction, User

from phillipa.emoji import (
    ALL_TRAINS,
    ANGRY,
    CONSTRUCTIONS,
    DOLPHIN,
    FLOWER,
    SOTON_SSAGO,
    SPAM,
    SSAGO,
)
from phillipa.trigger import (
    MessageRandomReactTrigger,
    MessageReactSendMessageTrigger,
    MessageRegexReactTrigger,
    SpecificUserReactTrigger,
    Trigger,
    UserMentionedReactTrigger,
)

LOGGER = logging.getLogger(__name__)


class PhillipaBot(Client):
    """
    Phillipa Discord Client.

    Receives events over websocket protocol and does stuff in response.
    """

    def __init__(
        self,
        good_keywords: List[str],
        bad_keywords: List[str],
        train_keywords: List[str],
    ):
        super().__init__()
        good_patterns: List[Pattern[str]] = [
            re.compile(kw, flags=re.IGNORECASE) for kw in good_keywords
        ]
        bad_patterns: List[Pattern[str]] = [
            re.compile(kw, flags=re.IGNORECASE) for kw in bad_keywords
        ]
        train_patterns: List[Pattern[str]] = [
            re.compile(kw, flags=re.IGNORECASE) for kw in train_keywords
        ]

        OLI = 678903558828982274
        LEON = 419109892272422932
        # DAN = 370197198589263874

        self.triggers: List[Trigger] = [
            SpecificUserReactTrigger(LEON, SPAM, 5),
            SpecificUserReactTrigger(OLI, SSAGO, 35),
            MessageRegexReactTrigger(bad_patterns, ANGRY),
            MessageRandomReactTrigger(train_patterns, list(ALL_TRAINS.values())),
            MessageRandomReactTrigger(
                [re.compile("build.?a.?rally", flags=re.IGNORECASE)],
                list(CONSTRUCTIONS.values()),
            ),
            MessageRegexReactTrigger(
                [
                    re.compile("the crown inn", flags=re.IGNORECASE),
                    re.compile("southampton", flags=re.IGNORECASE),
                    re.compile("soton", flags=re.IGNORECASE),
                ],
                SOTON_SSAGO,
            ),
            MessageRegexReactTrigger(
                [re.compile("dolphin", flags=re.IGNORECASE)], DOLPHIN,
            ),
            MessageRegexReactTrigger(good_patterns, FLOWER),
            MessageReactSendMessageTrigger(FLOWER, FLOWER),
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
        for trigger in self.triggers:
            result = await trigger.try_reaction(reaction, user)
            if result:
                return
