from fastapi import APIRouter, Depends
from dependencies.auth import verify_jwt
from services.http_client import http_get, http_post
from config import INTEGRATION_URL

router = APIRouter(tags=['Integrations'])


@router.get('/')
async def list_connectors(user_id=Depends(verify_jwt)):
    return await http_get(f'{INTEGRATION_URL}/connectors/{user_id}')


@router.post('/connect')
async def connect(data: dict, user_id=Depends(verify_jwt)):
    data['user_id'] = user_id
    return await http_post(f'{INTEGRATION_URL}/connect', json=data)
