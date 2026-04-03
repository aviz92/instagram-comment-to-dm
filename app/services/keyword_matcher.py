"""
Matches a comment text against configured trigger rules.
"""

from app.models.trigger_config import TriggerConfig, TriggerRule


class KeywordMatcher:
    def __init__(self, config: TriggerConfig) -> None:
        self._config = config

    def match(self, comment_text: str, post_id: str) -> TriggerRule | None:
        """
        Returns the first matching TriggerRule for (comment_text, post_id), or None.
        Rules scoped to a specific post_id take priority over global rules (post_id=None).
        """
        text = comment_text if self._config.rules and self._config.rules[0].case_sensitive else comment_text.lower()

        post_specific = [r for r in self._config.rules if r.post_id == post_id]
        global_rules = [r for r in self._config.rules if r.post_id is None]

        for rule in post_specific + global_rules:
            keyword = rule.keyword if rule.case_sensitive else rule.keyword.lower()
            if keyword in text:
                return rule

        return None
