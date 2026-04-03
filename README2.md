# instagram-comment-to-dm

Sends a private Instagram DM when a user comments a keyword on a post.

## How it works

1. User comments `LINK` (or any configured keyword) on your Instagram post
2. Meta sends a webhook event to this service
3. Service validates the event, checks for duplicates, and sends a DM

## Setup

### 1. Meta Developer App
- Create a Facebook App at https://developers.facebook.com
- Add **Instagram Graph API** product
- Connect your Instagram Business/Creator account via a Facebook Page
- Required permissions: `instagram_manage_comments`, `instagram_manage_messages`, `instagram_basic`

### 2. Local dev
```bash
cp .env.example .env
# fill in your tokens

uv sync
uv run uvicorn app.main:app --reload

# expose locally with ngrok:
ngrok http 8000
```

### 3. Webhook registration
Set webhook URL in Meta App Dashboard:
```
https://<your-ngrok-url>/webhooks
```
Subscribe to: `comments` field on the `instagram` object.

## Configure trigger rules

Edit `app/routers/webhooks.py` → `_config` (future: load from DB/config file):

```python
TriggerRule(
    keyword="LINK",
    reply_message="Hey! Here's the link 👉 https://example.com",
    post_id=None,  # None = apply to all posts
)
```
