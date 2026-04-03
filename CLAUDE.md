# CLAUDE.md — instagram-comment-to-dm

## Project Purpose
FastAPI service that sends a private Instagram DM when a user comments a keyword on a post.
Built as a weekend project by Avi Zaguri. Seed for a future `python-instagram-plus` library.

---

## Architecture

```
app/
├── main.py                        # FastAPI app + lifespan (DB init)
├── config.py                      # pydantic-settings from .env
├── db.py                          # SQLite via SQLModel — duplicate-DM prevention
├── routers/
│   ├── webhooks.py                # GET (verification) + POST (events) — MAIN LOGIC
│   └── health.py
├── services/
│   ├── instagram_client.py        # Graph API wrapper → future python-instagram-plus
│   ├── keyword_matcher.py         # keyword → TriggerRule matching
│   └── dm_sender.py               # orchestrator: match + dedup + send
└── models/
    ├── webhook_event.py           # Pydantic models for Meta webhook payload
    ├── trigger_config.py          # TriggerRule / TriggerConfig
    └── processed_dm.py            # SQLModel table — processed comment tracking
```

---

## Flow

```
POST /webhooks (Meta sends this on every comment)
    ↓
Signature verification (HMAC-SHA256 with app_secret)
    ↓
Parse comment: comment_id, text, commenter_user_id, post_id
    ↓
DMSender.handle_comment()
    ├── db.is_already_processed(comment_id) → skip if True
    ├── KeywordMatcher.match(text, post_id) → find matching TriggerRule
    └── InstagramClient.send_dm(commenter_user_id, rule.reply_message)
        └── db.mark_as_processed(...)
```

---

## Key Design Decisions

- **Duplicate prevention**: keyed on `comment_id` (unique per comment from Meta)
- **Rule priority**: post-specific rules before global rules (post_id=None)
- **Signature verification**: every POST verified via `x-hub-signature-256` header
- **No scheduler**: purely event-driven via Meta webhooks

---

## Environment Variables (.env)

| Variable | Description |
|---|---|
| `INSTAGRAM_ACCESS_TOKEN` | Long-lived Page Access Token |
| `INSTAGRAM_APP_SECRET` | Facebook App Secret (for HMAC verification) |
| `INSTAGRAM_VERIFY_TOKEN` | Your custom string for webhook verification handshake |
| `LOG_LEVEL` | `INFO` (default) |
| `DATABASE_URL` | `sqlite:///./instagram_trigger.db` (default) |

---

## Package Manager
Use `uv` for all package operations:
```bash
uv sync
uv run uvicorn app.main:app --reload
uv run pytest
```

---

## Dependencies
- `fastapi` + `uvicorn` — web framework
- `httpx` — async HTTP for Graph API calls
- `sqlmodel` — SQLite ORM for processed DM tracking
- `pydantic-settings` — .env management
- `custom-python-logger` — Avi's logger (aviz92 ecosystem)
- `python-custom-exceptions` — Avi's exceptions (aviz92 ecosystem)

---

## Open TODOs (next iterations)

- [ ] Load `TriggerRule` list from DB (admin CRUD endpoints) instead of hardcoded in `webhooks.py`
- [ ] Token refresh logic in `instagram_client.py`
- [ ] `/rules` admin router — POST/GET/DELETE trigger rules
- [ ] Extract `instagram_client.py` → standalone `python-instagram-plus` package
- [ ] Docker + docker-compose for deployment
- [ ] Add `pytest` tests for `keyword_matcher.py` and `dm_sender.py`

---

## Meta App Setup (for Claude Code context)

1. Facebook Developer App → Add Instagram Graph API product
2. Permissions needed: `instagram_manage_comments`, `instagram_manage_messages`, `instagram_basic`
3. Webhook: subscribe to `comments` field on `instagram` object
4. Local dev: use `ngrok http 8000` to expose the webhook endpoint
5. Webhook URL format: `https://<ngrok-url>/webhooks`

---

## Naming Convention (aviz92 ecosystem)
- Services: noun + action (e.g. `DMSender`, `KeywordMatcher`, `InstagramClient`)
- Models: descriptive SQLModel/Pydantic classes
- Config: all via `pydantic-settings` / `.env`
