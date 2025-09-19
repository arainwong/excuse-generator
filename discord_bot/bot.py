import discord
from discord import app_commands
from discord.ui import View, button
from scripts.excuse_generator import ExcuseGenerator
import json
import time

class ExcuseView(View):
    def __init__(self, config):
        super().__init__(timeout=None)
        self.config = config
        self.message_mode = config["MESSAGE_MODE"]
        self.good_reaction = config["GOOD_REACTION"]
        self.bad_reaction = config["BAD_REACTION"]
        self.change_button.label = config["BUTTON_LABEL"]

    @button(label="Some Placeholder", style=discord.ButtonStyle.primary)
    async def change_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        now = time.time()
        user_id = interaction.user.id

        # button press cooldowns check
        if user_id in cooldowns and now - cooldowns[user_id] < COOLDOWN_SECONDS:
            await interaction.response.defer()
            return
        cooldowns[user_id] = now

        # generate new excuse
        _, sample = g.generate()

        if self.message_mode == 'delete':
            await interaction.message.delete()
            new_msg = await interaction.channel.send(
                f"{sample}", view=ExcuseView(self.config)
            )
            await new_msg.add_reaction(self.good_reaction)
            await new_msg.add_reaction(self.bad_reaction)
        elif self.message_mode == 'keep':
            new_msg = await interaction.channel.send(
                f"{sample}", view=ExcuseView(self.config)
            )
            await new_msg.add_reaction(self.good_reaction)
            await new_msg.add_reaction(self.bad_reaction)
        else:
            raise KeyError("Unknown message mode. Please use 'keep' or 'delete'.")

        await interaction.response.defer()


class ExcuseBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Bot {self.user} online!")


if __name__ == "__main__":
    # read config
    with open("config/dicord_bot_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    TOKEN = config["DISCORD_TOKEN"]
    GOOD_REACTION = config["GOOD_REACTION"]
    BAD_REACTION = config["BAD_REACTION"]
    # avoid frequent user clicks 
    cooldowns = {}
    COOLDOWN_SECONDS = config["COOLDOWN_SECONDS"]

    intents = discord.Intents.default()
    intents.reactions = True

    g = ExcuseGenerator(csv_path="config/excuse_dictionary.csv")    

    client = ExcuseBot(intents=intents)

    @client.tree.command(name="excuse", description="游戏输了队友全责，我从不犯错！")
    async def excuse(interaction: discord.Interaction):
        _, sample = g.generate()
        # 1. send message
        await interaction.response.send_message(
            f"{sample}", view=ExcuseView(config)
        )
        # 2. add reaction
        sent_msg = await interaction.original_response()
        await sent_msg.add_reaction(GOOD_REACTION)
        await sent_msg.add_reaction(BAD_REACTION)

    client.run(TOKEN)
