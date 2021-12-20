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

    async def start(self):
        asyncio.create_task(self.send_scheduled_message_periodically())
        self.discord_client.on_ready = self.set_scheduled_messages
        print("Starting!")
        await self.discord_client.start(self.config.discord_bot_token)


if __name__ == '__main__':
    bot = Bot(Config.make(), discord.Client())
    asyncio.get_event_loop().run_until_complete(bot.start())
