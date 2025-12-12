from contextlib import asynccontextmanager

import socketio as _socketio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import SERVICE_NAME, CORS_ORIGINS, SOCKETIO_PATH
from database.connection import init_db
from deps import get_db
from database.repositories.conversations import list_conversations, create_conversation, get_conversation
from database.repositories.messages import list_messages, add_message
from schemas import ConversationOut, MessageOut, SendMessageIn
from sqlalchemy.ext.asyncio import AsyncSession

from socketio_app import sio, emit_message_to_chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


fastapi_app = FastAPI(title=SERVICE_NAME, version="1.0.0", lifespan=lifespan)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.get("/health")
async def health():
    return {"status": "ok"}


@fastapi_app.get("/conversations/{user_id}", response_model=list[ConversationOut])
async def api_list_conversations(user_id: str, db: AsyncSession = Depends(get_db)):
    items = await list_conversations(db, user_id=user_id)
    return items


@fastapi_app.post("/conversations/{user_id}", response_model=ConversationOut)
async def api_create_conversation(user_id: str, db: AsyncSession = Depends(get_db)):
    c = await create_conversation(db, user_id=user_id, platform="telegram")
    return c


@fastapi_app.get("/messages/{chat_id}", response_model=list[MessageOut])
async def api_get_messages(chat_id: str, db: AsyncSession = Depends(get_db), limit: int = 100):
    c = await get_conversation(db, chat_id)
    if not c:
        raise HTTPException(404, "Conversation not found")
    items = await list_messages(db, conversation_id=chat_id, limit=limit)
    return items


@fastapi_app.post("/messages/{chat_id}", response_model=MessageOut)
async def api_send_message(chat_id: str, payload: SendMessageIn, db: AsyncSession = Depends(get_db)):
    c = await get_conversation(db, chat_id)
    if not c:
        raise HTTPException(404, "Conversation not found")
    if c.user_id != payload.user_id:
        raise HTTPException(403, "Forbidden")

    try:
        msg = await add_message(db, conversation_id=chat_id, sender=payload.sender, text=payload.text)
    except ValueError:
        raise HTTPException(404, "Conversation not found")

    await emit_message_to_chat(chat_id, {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "sender": msg.sender,
        "text": msg.text,
        "timestamp": msg.timestamp.isoformat(),
        "is_ai_generated": msg.is_ai_generated,
    })

    return msg


app = _socketio.ASGIApp(sio, fastapi_app, socketio_path=SOCKETIO_PATH)
