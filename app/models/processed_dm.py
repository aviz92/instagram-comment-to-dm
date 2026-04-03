from datetime import datetime
from sqlmodel import Field, SQLModel


class ProcessedDM(SQLModel, table=True):
    """Tracks which (user, post) pairs have already received a DM — prevents duplicates."""

    id: int | None = Field(default=None, primary_key=True)
    instagram_user_id: str = Field(index=True)
    post_id: str = Field(index=True)
    comment_id: str = Field(unique=True)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
