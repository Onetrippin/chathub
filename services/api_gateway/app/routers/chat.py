from fastapi import APIRouter, Depends, Request
from dependencies.auth import verify_jwt
from services.http_client_with_context import ctx_get, ctx_post
from config import MESSAGE_URL

router = APIRouter(tags=["Chats"])


@router.get("/")
async def get_user_chats(request: Request, user_id=Depends(verify_jwt)):
    return await ctx_get(request, f"{MESSAGE_URL}/conversations/{user_id}")


@router.get("/{chat_id}/messages")
async def get_messages(request: Request, chat_id: str, user_id=Depends(verify_jwt)):
    return await ctx_get(request, f"{MESSAGE_URL}/messages/{chat_id}")


@router.post("/{chat_id}/messages")
async def send_message(request: Request, chat_id: str, data: dict, user_id=Depends(verify_jwt)):
    payload = dict(data)
    payload["user_id"] = user_id
    return await ctx_post(request, f"{MESSAGE_URL}/messages/{chat_id}", json=payload)
