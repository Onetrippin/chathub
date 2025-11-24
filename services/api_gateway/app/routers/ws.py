from fastapi import APIRouter, WebSocket, Depends
from dependencies.auth import verify_jwt
from services.websocket_proxy import ws_proxy

router = APIRouter(tags=['WebSocket'])


@router.websocket('/chat/{chat_id}')
async def ws_chat(websocket: WebSocket, chat_id: str, user_id=Depends(verify_jwt)):
    await ws_proxy(websocket, chat_id, user_id)
