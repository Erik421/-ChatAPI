from sqlalchemy.orm import Session
import models


def create_chat(db: Session, title: str):
    chat = models.Chat(title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int):
    return db.get(models.Chat, chat_id)


def create_message(db: Session, chat_id: int, text: str):
    msg = models.Message(chat_id=chat_id, text=text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_last_messages(db: Session, chat_id: int, limit: int):
    return (
        db.query(models.Message)
        .filter(models.Message.chat_id == chat_id)
        .order_by(models.Message.created_at.desc())
        .limit(limit)
        .all()
    )


def delete_chat(db: Session, chat: models.Chat):
    db.delete(chat)
    db.commit()
