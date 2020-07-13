"""Triggers for Phillipa."""
import re
from abc import ABCMeta
from random import choice, randint
from typing import List, Optional, Pattern, Union

from discord import ClientUser, Emoji, Message, Reaction, User


class Trigger(metaclass=ABCMeta):
    """A trigger for Phillipa, with an associated action."""

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it triggers."""
        return False

    async def try_reaction(self, reaction: Reaction, user: User) -> bool:
        """Try a reaction to see if it triggers."""
        return False


class MessageRegexReactTrigger(Trigger):
    """A trigger that will react to a message when words are found."""

    def __init__(self, pattern_list: List[str], emoji: Union[str, Emoji]) -> None:
        self.pattern_list = pattern_list
        self.regex_list: List[Pattern[str]] = [
            re.compile(x, flags=re.IGNORECASE) for x in pattern_list
        ]
        self.emoji = emoji

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it matches."""
        if match := self._message_matches(self.regex_list, message):
            await self.react(message)
        return match

    async def react(self, message: Message) -> None:
        """React with an emoji."""
        await message.add_reaction(self.emoji)

    def _message_matches(
        self, pattern_list: List[Pattern[str]], message: Message,
    ) -> bool:
        """Check if the message matches any of the patterns."""
        return any(
            self._message_compare(pattern, message.content) for pattern in pattern_list
        )

    def _message_compare(self, pattern: Pattern[str], content: str) -> bool:
        """Comparison function."""
        res = re.search(pattern, content) is not None
        return res

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pattern_list},emoji={self.emoji})"


class MessageRandomReactTrigger(MessageRegexReactTrigger):
    """React randomly to a message."""

    def __init__(self, pattern_list: List[str], emojis: List[str]) -> None:
        self.pattern_list = pattern_list
        self.regex_list: List[Pattern[str]] = [
            re.compile(x, flags=re.IGNORECASE) for x in pattern_list
        ]
        self.emojis = emojis

    async def react(self, message: Message) -> None:
        """React with an emoji."""
        await message.add_reaction(choice(self.emojis))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pattern_list},emojis={self.emojis})"


class UserMentionedReactTrigger(Trigger):
    """React when a specific user is mentioned."""

    def __init__(self, user: ClientUser, emoji: Union[str, Emoji]):
        self.user = user
        self.emoji = emoji

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it matches."""
        if match := self.user in message.mentions:
            await message.add_reaction(self.emoji)
        return match

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.user.name},emoji={self.emoji})"


class SpecificUserReactTrigger(Trigger):
    """React when a specific user speaks."""

    def __init__(
        self,
        user: int,
        emoji: Union[str, Emoji],
        *,
        chance: int = 1,
        trigger_word: str = "aberdennschaften832y4782mzsdh92",
        exclusive: bool = False,
        typing: bool = False,
    ):
        self.user = user
        self.emoji = emoji
        self.chance = chance
        self.trigger_word = trigger_word
        self.exclusive = exclusive
        self.typing = typing

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it matches."""
        if message.author.id == self.user:
            if any(
                [
                    randint(1, self.chance) == 1,
                    self.trigger_word in message.content.lower(),
                ],
            ):
                await message.add_reaction(self.emoji)
                if self.typing:
                    await message.channel.trigger_typing()
                return self.exclusive
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.user},emoji={self.emoji})"


class MessageReactSendMessageTrigger(Trigger):
    """Send the user a message when they react to a message."""

    def __init__(self, emoji: Union[str, Emoji], message: Optional[str] = None) -> None:
        self.emoji = emoji
        if message is None:
            self.message = emoji
        else:
            self.message = message

    async def try_reaction(
        self, reaction: Reaction, user: User, *, ignore_bots: bool = True,
    ) -> bool:
        """Try a reaction."""
        if ignore_bots and not user.bot or not ignore_bots:
            if reaction.emoji == self.emoji:
                await user.send(self.message)  # type: ignore
                return True
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(emoji={self.emoji}, message={self.message})"
