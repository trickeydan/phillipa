"""Triggers for Phillipa."""
import re
from abc import ABCMeta, abstractmethod
from typing import List, Pattern

from discord import ClientUser, Message, Reaction, User


class Trigger(metaclass=ABCMeta):
    """A trigger for Phillipa, with an associated action."""

    @abstractmethod
    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it triggers."""
        pass

    async def try_reaction(self, reaction: Reaction, user: User) -> bool:
        """Try a reaction to see if it triggers."""
        return False


class MessageRegexReactTrigger(Trigger):
    """A trigger that will react to a message when words are found."""

    def __init__(self, regex_list: List[Pattern[str]], emoji: str) -> None:
        self.regex_list = regex_list
        self.emoji = emoji

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it matches."""
        if match := self._message_matches(self.regex_list, message):
            await message.add_reaction(self.emoji)
        return match

    def _message_matches(
        self, pattern_list: List[Pattern[str]], message: Message,
    ) -> bool:
        """Check if the message matches any of the patterns."""
        return any(
            self._message_compare(pattern, message.content) for pattern in pattern_list
        )

    def _message_compare(self, pattern: Pattern[str], content: str) -> bool:
        """Comparison function."""
        return re.search(pattern, content) is not None


class UserMentionedReactTrigger(Trigger):
    """React when a specific user is mentioned."""

    def __init__(self, user: ClientUser, emoji: str):
        self.user = user
        self.emoji = emoji

    async def try_message(self, message: Message) -> bool:
        """Try a message to see if it matches."""
        print(self.user, message.mentions)
        if match := self.user in message.mentions:
            await message.add_reaction(self.emoji)
        return match
