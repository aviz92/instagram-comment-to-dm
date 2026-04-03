"""
Webhook router — handles both:
  GET  /webhooks  → Meta verification challenge
  POST /webhooks  → Real-time comment events
"""

import hashlib
import hmac
import json

from fastapi import APIRouter, HTTPException, Query, Request, status
from custom_python_logger import get_logger

from app.config import settings
from app.models.trigger_config import TriggerConfig, TriggerRule
from app.services.dm_sender import DMSender

logger = get_logger(__name__)
router = APIRouter(tags=["webhooks"])

# ---------------------------------------------------------------------------
# TODO: Load rules from DB / config file / env in a future iteration.
#       For now, define rules here directly.
# ---------------------------------------------------------------------------
_config = TriggerConfig(
    rules=[
        TriggerRule(
            keyword="LINK",
            reply_message="Hey! Here's the link you asked for 👉 https://your-link-here.com",
        ),
    ]
)
_sender = DMSender(config=_config)


def _verify_signature(payload: bytes, x_hub_signature: str) -> bool:
    """Validate that the webhook came from Meta."""
    expected = "sha256=" + hmac.new(
        settings.instagram_app_secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, x_hub_signature)


@router.get("/webhooks")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
) -> int:
    """Meta webhook verification handshake."""
    if hub_mode != "subscribe" or hub_verify_token != settings.instagram_verify_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verification failed")
    logger.info("Webhook verification successful")
    return int(hub_challenge)


@router.post("/webhooks")
async def receive_webhook(request: Request) -> dict:
    """Receive and process Instagram comment events."""
    body = await request.body()

    signature = request.headers.get("x-hub-signature-256", "")
    if not _verify_signature(body, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

    payload = json.loads(body)

    if payload.get("object") != "instagram":
        return {"status": "ignored"}

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            if change.get("field") != "comments":
                continue

            value = change.get("value", {})
            comment_id = value.get("id")
            comment_text = value.get("text", "")
            commenter_id = value.get("from", {}).get("id")
            post_id = value.get("media", {}).get("id")

            if not all([comment_id, commenter_id, post_id]):
                logger.warning(f"Incomplete comment event — skipping: {value}")
                continue

            await _sender.handle_comment(
                comment_id=comment_id,
                comment_text=comment_text,
                commenter_user_id=commenter_id,
                post_id=post_id,
            )

    return {"status": "ok"}
