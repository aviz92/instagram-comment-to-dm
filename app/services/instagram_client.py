"""
Instagram Graph API client.
This module is the seed for python-instagram-plus.

Responsibilities:
- Send DMs via /me/messages
- Fetch comment details if needed
- Handle token refresh (TODO)
"""

import httpx
from custom_python_logger import get_logger

from app.config import settings

logger = get_logger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v20.0"


class InstagramClient:
    def __init__(self, access_token: str = settings.instagram_access_token) -> None:
        self._token = access_token
        self._client = httpx.AsyncClient(base_url=GRAPH_API_BASE, timeout=10.0)

    async def send_dm(self, recipient_instagram_user_id: str, message: str) -> dict:
        """
        Send a DM to an Instagram user via the Messenger API.
        Requires: instagram_manage_messages permission.
        Docs: https://developers.facebook.com/docs/messenger-platform/instagram/features/send-message
        """
        payload = {
            "recipient": {"id": recipient_instagram_user_id},
            "message": {"text": message},
            "access_token": self._token,
        }
        logger.info(f"Sending DM to user {recipient_instagram_user_id}")
        response = await self._client.post("/me/messages", json=payload)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()
