from fastapi import APIRouter, Depends
from dependencies.auth import verify_jwt
from services.http_client import http_get, http_post
from config import USER_URL

router = APIRouter(tags=['Users'])


@router.get('/me')
async def get_profile(user_id=Depends(verify_jwt)):
    return await http_get(f'{USER_URL}/profiles/{user_id}')


@router.post('/me/settings')
async def update_settings(data: dict, user_id=Depends(verify_jwt)):
    return await http_post(f'{USER_URL}/settings/{user_id}', json=data)
