from pydantic import BaseModel


class CommentValue(BaseModel):
    id: str
    text: str
    from_: dict | None = None    # {"id": "...", "username": "..."}
    media: dict | None = None    # {"id": "...", "media_product_type": "..."}

    model_config = {"populate_by_name": True}


class WebhookEntry(BaseModel):
    id: str
    time: int
    changes: list[dict]


class WebhookPayload(BaseModel):
    object: str          # "instagram"
    entry: list[WebhookEntry]
