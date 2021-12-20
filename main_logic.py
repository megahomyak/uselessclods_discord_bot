import asyncio
import datetime
from typing import NoReturn, Optional

import discord

import utils
from config import Config


class Bot:

    def __init__(self, config: Config, discord_client: discord.Client):
        self.config = config
        self.discord_client = discord_client
        self.mentions_channel: Optional[discord.TextChannel] = None
        self.role_to_set: Optional[discord.Role] = None

    async def send_scheduled_message_periodically(self) -> NoReturn:
        while True:
            for future_day_index in self.config.day_indexes:
                now = utils.now()
                future = now + datetime.timedelta(
                    days=utils.get_amount_of_days_to_a_weekday(
                        current_weekday_index=now.weekday(),
                        future_weekday_index=future_day_index
                    )
                )
                future = future.replace(
                    hour=self.config.moscow_message_hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )
                await asyncio.sleep((future - now).total_seconds())
                await self.mentions_channel.send(self.config.scheduled_message)

    async def set_scheduled_messages(self):
        self.mentions_channel = self.discord_client.get_channel(
            self.config.scheduled_messages_channel_id
        )
        for role in self.mentions_channel.guild.roles:
            if role.name == self.config.role_name:
                self.role_to_set = role
                break
        else:
            print(f"No role named {self.config.role_name} found!")
            exit()

    async def handle_raw_reaction(
            self, reaction: discord.RawReactionActionEvent):
        if self.config.debug:
            print("New reaction!", reaction)
        if (
            reaction.emoji.name == self.config.emoji_trigger_name
            and reaction.emoji.id == self.config.emoji_trigger_id
            and reaction.channel_id == self.mentions_channel.id
        ):
            message = await self.mentions_channel.fetch_message(
                reaction.message_id
            )
            if str(message.author) == self.config.discord_bot_nickname:
                member: discord.Member = (
                    await self.mentions_channel.guild.fetch_member(
                        reaction.user_id
                    )
                )
                if reaction.event_type == "REACTION_ADD":
                    await member.add_roles(self.role_to_set)
                else:
                    await member.remove_roles(self.role_to_set)

    async def handle_incoming_discord_message(self, message: discord.Message):
        if self.config.debug:
            print(
                f"New message arrived! Channel id: {message.channel.id}, "
                f"text: {message.content}"
            )
        if message.content == "/send_emojis_message":
            await message.channel.send(self.config.emoji_trigger_message)

    async def start(self):
        asyncio.create_task(self.send_scheduled_message_periodically())
        self.discord_client.on_ready = self.set_scheduled_messages
        self.discord_client.on_message = self.handle_incoming_discord_message
        self.discord_client.on_raw_reaction_add = self.handle_raw_reaction
        self.discord_client.on_raw_reaction_remove = self.handle_raw_reaction
        print("Starting!")
        await self.discord_client.start(self.config.discord_bot_token)


if __name__ == '__main__':
    bot = Bot(Config.make(), discord.Client())
    asyncio.get_event_loop().run_until_complete(bot.start())
