import json
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    discord_bot_token: str
    scheduled_message: str
    day_indexes: List[int]
    moscow_message_hour: int
    scheduled_messages_channel_id: int

    @classmethod
    def make(cls):
        return cls(**json.load(open("config.json", encoding="utf-8")))
