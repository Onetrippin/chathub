from fastapi import APIRouter
from services.http_client import http_post
from config import AUTH_URL

router = APIRouter(tags=['Auth'])


@router.post('/telegram/login')
async def telegram_login(data: dict):
    return await http_post(f'{AUTH_URL}/telegram/login', json=data)
