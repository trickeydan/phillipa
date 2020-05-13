import discord
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)


class PhillipaBot(discord.Client):

    def __init__(self, good_keywords, bad_keywords):
        super().__init__()

        self.good_keywords = good_keywords
        self.bad_keywords = bad_keywords

    async def on_ready(self):
        logging.info(f"Connected as {self.user}")

    async def on_message(self, message):
        
        content = message.content.lower()

        good_conditions = []

        good_conditions.append(self.user in message.mentions)

        for word in self.good_keywords:
            good_conditions.append(word in content)

        bad_conditions = []

        for word in self.bad_keywords:
            bad_conditions.append(word in content)

        if any(good_conditions) and not any(bad_conditions):
            logging.info("I like")
            await message.add_reaction("💮")

        if any(bad_conditions):
            logging.info("I dislike")
            await message.add_reaction("😠")

    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.emoji == "💮":
            logging.info(f"{user} is nice.")
            await user.send("💮")

def load_words(filename):
    path = Path(filename)
    with path.open() as fh:
        return fh.read().split("\n")

if __name__ == "__main__":
    logging.info("Starting Phillipa")
    good = load_words("good.txt")
    bad = load_words("bad.txt")
    client = PhillipaBot(good, bad)
    token = os.environ.get('DISCORD_TOKEN', "NzEwMjMyOTg0NTk0MTUzNDcz.XrxgtA.IhI32vh8JZtlzWqCGQER_nRGzyY")
    client.run(token)
