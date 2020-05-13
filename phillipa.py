import discord
import logging
import os

logging.basicConfig(level=logging.INFO)

GOOD_KEYWORDS = [
    "dolphin",
    "phil",
    "phillipa",
    "rishi",
    "jesters",
    "bills bills bills",
    "the crown inn",
    "southampton",
    "soton",
    "flower",
    "baa",
    "number ten",
    "number 10",
    "bin",
    "build-a-rally",
    "build a rally",
]

BAD_KEYWORDS = [
    "portsmouth",
    "fishing net",
    "stupid pink thing",
    "nasty pink thing",
    "pink thing",
]

class PhillipaBot(discord.Client):

    async def on_ready(self):
        logging.info(f"Connected as {self.user}")

    async def on_message(self, message):
        
        content = message.content.lower()

        good_conditions = []

        good_conditions.append(self.user in message.mentions)

        for word in GOOD_KEYWORDS:
            good_conditions.append(word in content)

        bad_conditions = []

        for word in BAD_KEYWORDS:
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

if __name__ == "__main__":
    logging.info("Starting Phillipa")
    client = PhillipaBot()
    token = os.environ.get('DISCORD_TOKEN', "NzEwMjMyOTg0NTk0MTUzNDcz.XrxgtA.IhI32vh8JZtlzWqCGQER_nRGzyY")
    client.run(token)
