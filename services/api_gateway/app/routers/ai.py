from fastapi import APIRouter, Depends
from dependencies.auth import verify_jwt
from services.http_client import http_post
from config import AI_URL

router = APIRouter(tags=['AI'])


@router.post('/{chat_id}/suggest')
async def suggest(chat_id: str, body: dict, user_id=Depends(verify_jwt)):
    body['user_id'] = user_id
    return await http_post(f'{AI_URL}/suggest/{chat_id}', json=body)


@router.post('/{chat_id}/summaries/bulk')
async def bulk_summary(chat_id: str, body: dict, user_id=Depends(verify_jwt)):
    body['user_id'] = user_id
    return await http_post(f'{AI_URL}/summaries/bulk/{chat_id}', json=body)
