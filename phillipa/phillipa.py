"""Phillipa the Dolphin Discord Bot."""
import logging
from typing import List

from discord import Activity, ActivityType, Message, Reaction, User
from discord.ext.commands import Bot
from discord.utils import get

from phillipa.emoji import (
    ALL_TRAINS,
    ANGRY,
    CARTWHEEL,
    CONSTRUCTIONS,
    CROWN,
    DOLPHIN,
    FLAMINGO,
    FLOWER,
    HEART,
    PAWPRINTS,
    PICKAXE,
    PINEAPPLE,
    PRIDE,
    SAD,
    SPAM,
    SWISS_FLAG,
    T_REX,
    WHITE_FLOWER,
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


class PhillipaBot(Bot):  # type: ignore
    """
    Phillipa Discord Bot.

    Receives events over websocket protocol and does stuff in response.
    """

    def __init__(self) -> None:
        super().__init__("gophillipa:")
        self.triggers: List[Trigger] = []

    async def on_ready(self) -> None:
        """Called when bot is connected."""
        LOGGER.info(f"Connected as {self.user}")
        await self.change_presence(
            activity=Activity(type=ActivityType.playing, name="in the waves"),
        )
        self._setup_triggers()

        for trigger in self.triggers:
            LOGGER.info(f"Added trigger: {trigger}")

    async def on_message(self, message: Message) -> None:
        """Message received."""
        for trigger in self.triggers:
            result = await trigger.try_message(message)
            if result:
                LOGGER.info(f'"{message.content}" -> {trigger}')
                return

    async def on_reaction_add(self, reaction: Reaction, user: User) -> None:
        """Reaction added to message in cache."""
        for trigger in self.triggers:
            result = await trigger.try_reaction(reaction, user)
            if result:
                LOGGER.info(f"{reaction.emoji} -> {trigger}")
                return

    def _setup_triggers(self) -> None:
        """Setup the triggers."""
        OLI = 678903558828982274
        LEON = 419109892272422932
        ELIZABETH = 725806119661863053
        AMBIBUG = 150782326345957390
        MYTHILLI = 689470333140336655
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

        WITAN = get(self.emojis, name="Witan") or "❓"
        SSAGO = get(self.emojis, name="ssago") or "❓"
        SOTON_SSAGO = get(self.emojis, name="southampton") or "❓"

        self.triggers = [
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
            SpecificUserReactTrigger(YOULBURY, WITAN, chance=5),
            MessageRegexReactTrigger(["witan"], HEART, chance=20),
            MessageRegexReactTrigger(
                ["kandersteg", "kisc", "switzerland"], WITAN, chance=20,
            ),
            MessageReactSendMessageTrigger(WITAN, str(WITAN) + HEART + SWISS_FLAG),
            # Build a rally
            MessageRandomReactTrigger(
                ["build.?a.?rally", "construction", "digger"],
                list(CONSTRUCTIONS.values()),
            ),
            # Southampton SSAGO
            MessageRegexReactTrigger(
                ["the crown inn", "southampton", "soton"], SOTON_SSAGO,
            ),
            MessageRegexReactTrigger(["dolphin"], DOLPHIN),
            # Trains
            MessageRandomReactTrigger(
                [
                    "train",
                    "locomotive",
                    "railway",
                    "train station",
                    "carriage",
                    "maglev",
                    "train driver",
                    "train guard",
                    "kings cross",
                    "waterloo",
                    "main line",
                    "oyster card",
                    "london underground",
                ],
                list(ALL_TRAINS.values()),
            ),
            MessageReactSendMessageTrigger(
                ALL_TRAINS["LOCOMOTIVE"],
                ALL_TRAINS["LOCOMOTIVE"] + (ALL_TRAINS["RAILWAY_CAR"] * 6),
            ),
            # Generic
            MessageRegexReactTrigger(["bad phillipa", "naughty phillipa"], SAD),
            MessageRegexReactTrigger(["pineapple"], PINEAPPLE),
            MessageRegexReactTrigger(["minecraft", "meinkraft"], PICKAXE),
            MessageRegexReactTrigger(["cartwheel", "dizzy"], CARTWHEEL),
            MessageRegexReactTrigger(["dog", "good boy"], PAWPRINTS),
            MessageRegexReactTrigger(
                [
                    "phil(lipa)?",
                    "rishi",
                    "jesters",
                    "(bills ){2}bills",
                    "flower",
                    "baa+",
                    "number ten",
                    "number 10",
                    "fish pie",
                    "christmas cake",
                    "cheese salad",
                    "rack of ribs",
                ],
                FLOWER,
            ),
            MessageRegexReactTrigger(
                ["portsmouth", "fishing net", "pink thing", "politics"], ANGRY,
            ),
            MessageReactSendMessageTrigger(FLOWER, FLOWER),
            MessageReactSendMessageTrigger(WHITE_FLOWER, FLOWER),
            UserMentionedReactTrigger(self.user, FLOWER),
            MessageRegexReactTrigger(["ssago"], SSAGO, chance=10),
        ]
