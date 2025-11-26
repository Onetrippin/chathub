from fastapi import Header, HTTPException
from services.http_client import http_get
from config import AUTH_URL


async def verify_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, 'Missing Authorization header')

    token = authorization.replace('Bearer ', '')

    result = await http_get(f'{AUTH_URL}/internal/verify', headers={'Authorization': f'Bearer {token}'})

    if not result.get('valid'):
        raise HTTPException(401, 'Invalid token')

    return result['user_id']
