from fastapi import APIRouter, Depends
from dependencies.auth import verify_jwt
from services.http_client import http_get, http_post
from config import MESSAGE_URL

router = APIRouter(tags=['Chats'])


@router.get('/')
async def get_user_chats(user_id=Depends(verify_jwt)):
    return await http_get(f'{MESSAGE_URL}/conversations/{user_id}')


@router.get('/{chat_id}/messages')
async def get_messages(chat_id: str, user_id=Depends(verify_jwt)):
    return await http_get(f'{MESSAGE_URL}/messages/{chat_id}')


@router.post('/{chat_id}/messages')
async def send_message(chat_id: str, data: dict, user_id=Depends(verify_jwt)):
    data['user_id'] = user_id
    return await http_post(f'{MESSAGE_URL}/messages/{chat_id}', json=data)
