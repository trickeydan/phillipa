import discord

GOOD_KEYWORDS = ["dolphin", "phil", "phillipa", "rishi", "jesters", "bills bills bills", "the crown inn", "southampton", "soton"]
BAD_KEYWORDS = ["portsmouth"]


class PhillipaBot(discord.Client):

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
            await message.add_reaction("💮")

        if any(bad_conditions):
            await message.add_reaction("😠")

    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.emoji == "💮":
            await user.send("💮")

client = PhillipaBot()

client.run("NzA3NjYyNjEwMTk5MzQ3Mjgx.XrMFiQ.BsSGHNDGhlAQzsjesBZhQKxEnV0")
