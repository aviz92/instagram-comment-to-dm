"""
Orchestrates the full comment → DM flow.
Called by the webhook router after signature verification.
"""

from custom_python_logger import get_logger

from app import db
from app.models.trigger_config import TriggerConfig
from app.services.instagram_client import InstagramClient
from app.services.keyword_matcher import KeywordMatcher

logger = get_logger(__name__)


class DMSender:
    def __init__(self, config: TriggerConfig) -> None:
        self._matcher = KeywordMatcher(config)
        self._client = InstagramClient()

    async def handle_comment(
        self,
        comment_id: str,
        comment_text: str,
        commenter_user_id: str,
        post_id: str,
    ) -> bool:
        """
        Returns True if a DM was sent, False otherwise.
        """
        if db.is_already_processed(comment_id):
            logger.debug(f"Comment {comment_id} already processed — skipping")
            return False

        rule = self._matcher.match(comment_text, post_id)
        if not rule:
            logger.debug(f"No matching rule for comment: '{comment_text}'")
            return False

        logger.info(f"Keyword '{rule.keyword}' matched — sending DM to {commenter_user_id}")
        await self._client.send_dm(commenter_user_id, rule.reply_message)

        db.mark_as_processed(
            instagram_user_id=commenter_user_id,
            post_id=post_id,
            comment_id=comment_id,
        )
        return True

    async def close(self) -> None:
        await self._client.close()
