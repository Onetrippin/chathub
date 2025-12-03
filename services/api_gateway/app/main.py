from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import auth, user, chat, ai, integration, ws
from config import GATEWAY_TITLE, GATEWAY_VERSION
from services.http_client import init_http_client, close_http_client
from middlewares.request_id import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_http_client()
    yield
    await close_http_client()


app = FastAPI(title=GATEWAY_TITLE, version=GATEWAY_VERSION, lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users")
app.include_router(chat.router, prefix="/chats")
app.include_router(ai.router, prefix="/ai")
app.include_router(integration.router, prefix="/integrations")
app.include_router(ws.router, prefix="/ws")


@app.get("/health")
async def health():
    return {"status": "ok"}
