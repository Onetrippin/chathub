from fastapi import FastAPI
from routers import auth, user, chat, ai, integration, ws

app = FastAPI(title='API Gateway', version='1.0.0')

app.include_router(auth.router, prefix='/auth')
app.include_router(user.router, prefix='/users')
app.include_router(chat.router, prefix='/chats')
app.include_router(ai.router, prefix='/ai')
app.include_router(integration.router, prefix='/integrations')
app.include_router(ws.router, prefix='/ws')


@app.get('/health')
async def health():
    return {'status': 'ok'}
