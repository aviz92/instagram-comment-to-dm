from sqlmodel import Session, SQLModel, create_engine, select

from app.config import settings
from app.models.processed_dm import ProcessedDM

engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def is_already_processed(comment_id: str) -> bool:
    with Session(engine) as session:
        result = session.exec(select(ProcessedDM).where(ProcessedDM.comment_id == comment_id)).first()
        return result is not None


def mark_as_processed(instagram_user_id: str, post_id: str, comment_id: str) -> None:
    with Session(engine) as session:
        record = ProcessedDM(
            instagram_user_id=instagram_user_id,
            post_id=post_id,
            comment_id=comment_id,
        )
        session.add(record)
        session.commit()
