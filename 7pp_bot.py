import discord
import random
import re
import os

# DICE_SIZES lists the available sizes of dice, as well as what distribution of symbols they use.
DICE_SIZES = {
    6: {"values": "regular"},
    8: {"values": "regular"},
    10: {"values": "regular"},
    12: {"values": "regular"},
    20: {"values": "solar"},
}

# DICE_VALUES is a dict of the different distributions of symbols.
DICE_VALUES = {
    "regular": {
        1: "salt",
        2: "jupiter",
        3: "jupiter",
        4: "jupiter",
        5: "mars",
        6: "venus",
        7: "mercury",
        8: "luna",
        9: "saturn",
        10: "neptune",
        11: "sol",
        12: "the devil",
    },
    "solar": {
        1: "the devil",
        2: "the devil",
        3: "the devil",
        4: "jupiter",
        5: "jupiter",
        6: "mars",
        7: "mars",
        8: "venus",
        9: "venus",
        10: "mercury",
        11: "mercury",
        12: "luna",
        13: "luna",
        14: "saturn",
        15: "saturn",
        16: "neptune",
        17: "neptune",
        18: "sol",
        19: "sol",
        20: "sol",
    },
}

# SYMBOLS is a map from symbol names to unicode characters
SYMBOLS = {
    "salt": "🜔",
    "jupiter": "♃",
    "mars": "♂",
    "venus": "♀",
    "mercury": "☿",
    "luna": "☾",
    "saturn": "♄",
    "neptune": "♆",
    "sol": "☉",
    "the devil": "🜍",
}

# MIN_DICE and MAX_DICE to prevent crazy long-running operations
MIN_DICE = 1
MAX_DICE = 100


class Client(discord.Client):
    # Set our discord presence to "Listening for !cast XdY"
    async def on_ready(self):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!cast XdY"))

    # When we receive a message
    async def on_message(self, message: discord.Message):

        # Try to match the message against a regex: "!cast {number}d{size}"
        # (We capture X and Y with capturing groups)
        roll_command = re.fullmatch("!cast ([0-9]+)d([0-9]+)", message.content)

        # If it matched:
        if roll_command:
            # Extract {number} and {size} from the command
            number, size = [int(i) for i in roll_command.group(1, 2)]

            # Check that the number of dice is sensible
            if number < MIN_DICE or number > MAX_DICE:
                await message.reply(
                    content=f"Invalid number of dice, pick a value bewteen {MIN_DICE} and {MAX_DICE}!"
                )
                return

            # Check whether the dice size exists
            if size not in DICE_SIZES.keys():
                await message.reply(
                    content=f"Invalid dice size, choose from {str(sorted(list(DICE_SIZES.keys())))}!"
                )
                return

            # Roll the dice!
            results = sorted([random.randint(1, size) for i in range(number)])

            # Replace the values with their results looked up in SYMBOLS
            results = [
                SYMBOLS[DICE_VALUES[DICE_SIZES[size]["values"]][i]] for i in results
            ]

            # Reply with a heading-sized code block. I think it looks nicest! :D
            await message.reply(content=f"# `{' '.join(results)}`")

            # The command is done!
            return

        # Try to match against "!help"
        help_command = re.fullmatch("!help", message.content)
        if help_command:
            await message.reply(
                content= "- `!help`: display this message\n"
                "- `!cast {number}d{size}`: roll `{number}` dice with `{size}` faces each"
            )

            # And we're done!
            return

if __name__ == "__main__":
    # We need to tell discord what permissions our bot wants
    # We just want the permission to read messages
    intents = discord.Intents.default()
    intents.message_content = True

    # Create a client with those intents, and run it
    client = Client(intents=intents)
    client.run(os.environ["DISCORD_TOKEN"])