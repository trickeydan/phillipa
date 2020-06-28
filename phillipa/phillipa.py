"""Phillipa the Dolphin Discord Bot."""
import logging
import re
from typing import List, Pattern

from discord import Activity, ActivityType, Client, Message, Reaction, User

from phillipa.emoji import (
    ALL_TRAINS,
    ANGRY,
    CONSTRUCTIONS,
    # CROWN,
    DOLPHIN,
    FLAMINGO,
    FLOWER,
    HEART,
    PRIDE,
    SOTON_SSAGO,
    SPAM,
    SSAGO,
    T_REX,
    WHITE_FLOWER,
    WITAN,
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
        ELIZABETH = 725806119661863053
        AMBIBUG = 150782326345957390 
        MYTHILLI = 726481072430252053
        DAN = 370197198589263874
        THOMAS_PUGS = 114830573914161158
        REX = 689409878162145280
        JOSH = 719651119952953436
        LAUREN = 725098884120051782
        LAURA_EGGS = 630765434416660481
        MUFFIN_MAN = 281404242579816448
        ETHAN = 719650891187094138
        YOULBURY = 690594174365335568

        self.triggers: List[Trigger] = [
            SpecificUserReactTrigger(
                LEON,
                SPAM,
                chance=3,
                trigger_word="spam",
                typing=True,
            ),
            SpecificUserReactTrigger(OLI, SSAGO, chance=35),
            SpecificUserReactTrigger(ELIZABETH, HEART, chance=10),
            SpecificUserReactTrigger(MYTHILLI, WHITE_FLOWER, chance=30, exclusive=True),
            SpecificUserReactTrigger(MYTHILLI, FLAMINGO, chance=30, exclusive=True),

            SpecificUserReactTrigger(DAN, PRIDE, chance=1),
            SpecificUserReactTrigger(THOMAS_PUGS, PRIDE, chance=1),
            SpecificUserReactTrigger(AMBIBUG, PRIDE, chance=1),
            SpecificUserReactTrigger(LAURA_EGGS, PRIDE, chance=1),
            SpecificUserReactTrigger(MUFFIN_MAN, PRIDE, chance=1),
            
            SpecificUserReactTrigger(REX, T_REX, chance=5),
            SpecificUserReactTrigger(JOSH, WITAN, chance=10, trigger_word="witan"),
            SpecificUserReactTrigger(LAUREN, WITAN, chance=100, trigger_word="witan"),
            SpecificUserReactTrigger(ETHAN, WITAN, chance=100, trigger_word="witan"),
            SpecificUserReactTrigger(YOULBURY, WITAN, chance=1, trigger_word="witan"),
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
            MessageReactSendMessageTrigger(WHITE_FLOWER, FLOWER),
            MessageReactSendMessageTrigger(
                ALL_TRAINS["LOCOMOTIVE"],
                ALL_TRAINS["LOCOMOTIVE"] + (ALL_TRAINS["RAILWAY_CAR"] * 6),
                ),
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
