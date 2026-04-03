from pydantic import BaseModel


class TriggerRule(BaseModel):
    """One keyword → one DM message, scoped to a specific post (or global if post_id is None)."""

    keyword: str                   # e.g. "LINK", "YES", "INFO"
    reply_message: str             # the DM body to send
    post_id: str | None = None     # None = apply to ALL posts
    case_sensitive: bool = False


class TriggerConfig(BaseModel):
    """Full set of rules loaded from config / env / future DB."""

    rules: list[TriggerRule] = []
