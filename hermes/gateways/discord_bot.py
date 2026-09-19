import os
from typing import Any, Dict

class DiscordGatewayAdapter:
    """
    Discord Bot Gateway Adapter.
    Enables remote command & multi-agent prompting directly from dedicated Discord channels.
    """
    def __init__(self, bot_token: str | None = None, channel_id: str | None = None):
        self.bot_token = bot_token or os.getenv("DISCORD_BOT_TOKEN", "")
        self.channel_id = channel_id or os.getenv("DISCORD_CHANNEL_ID", "")

    def format_discord_embed(self, title: str, description: str, color: int = 0x89B4FA) -> Dict[str, Any]:
        return {
            "title": title,
            "description": description,
            "color": color,
            "footer": {"text": "HermesAG Autonomous Discord Daemon"}
        }

    async def handle_incoming_message(self, author: str, content: str) -> Dict[str, Any]:
        return {
            "reply": f"Hermes received: '{content}' from {author}. Routing to cognitive engine.",
            "status": "queued"
        }
