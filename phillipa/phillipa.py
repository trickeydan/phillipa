"""Phillipa the Dolphin Discord Bot."""
import logging
from typing import List

from discord import Activity, ActivityType, Client, Message, Reaction, User

from phillipa.emoji import (
    ALL_TRAINS,
    ANGRY,
    CONSTRUCTIONS,
    CROWN,
    DOLPHIN,
    FLAMINGO,
    FLOWER,
    HEART,
    PICKAXE,
    PRIDE,
    SOTON_SSAGO,
    SPAM,
    SWISS_FLAG,
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

        OLI = 678903558828982274
        LEON = 419109892272422932
        ELIZABETH = 725806119661863053
        AMBIBUG = 150782326345957390
        MYTHILLI = 726481072430252053
        THOMAS_PUGS = 114830573914161158
        REX = 689409878162145280
        JOSH = 719651119952953436
        LAUREN = 725098884120051782
        ETHAN = 719650891187094138
        YOULBURY = 690594174365335568

        DAN = 370197198589263874
        # LAURA_EGGS = 630765434416660481
        # MUFFIN_MAN = 281404242579816448
        # PIPSTER = 674784774669467663

        self.triggers: List[Trigger] = [

            # People
            SpecificUserReactTrigger(
                LEON, SPAM, chance=2, trigger_word="spam", typing=True,
            ),
            SpecificUserReactTrigger(OLI, SSAGO, chance=35),
            SpecificUserReactTrigger(ELIZABETH, HEART, chance=10),
            SpecificUserReactTrigger(MYTHILLI, WHITE_FLOWER, chance=10, exclusive=True),
            SpecificUserReactTrigger(MYTHILLI, FLAMINGO, chance=10, exclusive=True),
            SpecificUserReactTrigger(DAN, PRIDE, chance=50),
            SpecificUserReactTrigger(THOMAS_PUGS, PRIDE, chance=50),
            SpecificUserReactTrigger(AMBIBUG, CROWN, chance=5, trigger_word="skribbl"),
            SpecificUserReactTrigger(REX, T_REX, chance=3),

            # Witan
            SpecificUserReactTrigger(JOSH, WITAN, chance=5),
            SpecificUserReactTrigger(LAUREN, WITAN, chance=5),
            SpecificUserReactTrigger(ETHAN, WITAN, chance=5),
            SpecificUserReactTrigger(YOULBURY, WITAN, chance=1),
            MessageRegexReactTrigger(["witan"], HEART),
            MessageRandomReactTrigger(
                ["kandersteg", "kisc", "switzerland"], WITAN,
            ),
            MessageReactSendMessageTrigger(WITAN, WITAN + HEART + SWISS_FLAG),

            

            # Build a rally
            MessageRandomReactTrigger(
                ["build.?a.?rally", "construction", "digger"], list(CONSTRUCTIONS.values()),
            ),

            # Southampton SSAGO
            MessageRegexReactTrigger(
                ["the crown inn", "southampton", "soton"],
                SOTON_SSAGO,
            ),
            MessageRegexReactTrigger(["dolphin"], DOLPHIN),

            # Trains
            MessageRandomReactTrigger(train_keywords, list(ALL_TRAINS.values())),
            MessageReactSendMessageTrigger(
                ALL_TRAINS["LOCOMOTIVE"],
                ALL_TRAINS["LOCOMOTIVE"] + (ALL_TRAINS["RAILWAY_CAR"] * 6),
            ),

            # Generic
            MessageRegexReactTrigger(["minecraft"], PICKAXE),
            MessageRegexReactTrigger(good_keywords, FLOWER),
            MessageRegexReactTrigger(bad_keywords, ANGRY),
            MessageRegexReactTrigger(["ssago"], SSAGO),   
            MessageReactSendMessageTrigger(FLOWER, FLOWER),
            MessageReactSendMessageTrigger(WHITE_FLOWER, FLOWER),
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
