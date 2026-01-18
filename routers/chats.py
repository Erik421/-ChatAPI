from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import crud

router = APIRouter(prefix="/chats", tags=["chats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=schemas.ChatOut,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(payload: schemas.ChatCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db, payload.title)


@router.post(
    "/{chat_id}/messages/",
    response_model=schemas.MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    chat_id: int,
    payload: schemas.MessageCreate,
    db: Session = Depends(get_db),
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return crud.create_message(db, chat_id, payload.text)


@router.get("/{chat_id}", response_model=schemas.ChatOut)
def get_chat(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = crud.get_last_messages(db, chat_id, limit)

    return schemas.ChatOut(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at,
        messages=list(reversed(messages)),
    )


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    crud.delete_chat(db, chat)
    return None
