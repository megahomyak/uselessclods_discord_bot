import json
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    discord_bot_token: str
    scheduled_message: str
    discord_bot_nickname: str
    day_indexes: List[int]
    moscow_message_hour: int
    scheduled_messages_channel_id: int
    debug: bool
    emoji_trigger_name: str
    emoji_trigger_message: str
    emoji_trigger_id: int
    role_name: str

    @classmethod
    def make(cls):
        return cls(**json.load(open("config.json", encoding="utf-8")))
