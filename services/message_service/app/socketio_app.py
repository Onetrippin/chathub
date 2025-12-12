import socketio
from config import REDIS_URL, SOCKETIO_NAMESPACE

mgr = socketio.AsyncRedisManager(REDIS_URL)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    client_manager=mgr,
    logger=False,
    engineio_logger=False,
)

def user_room(user_id: str) -> str:
    return f"user:{user_id}"

def chat_room(chat_id: str) -> str:
    return f"chat:{chat_id}"


@sio.event(namespace=SOCKETIO_NAMESPACE)
async def connect(sid, environ, auth):
    qs = environ.get("QUERY_STRING", "")
    params = dict(x.split("=", 1) for x in qs.split("&") if "=" in x)
    user_id = params.get("user_id")
    if not user_id:
        return False
    await sio.save_session(sid, {"user_id": user_id}, namespace=SOCKETIO_NAMESPACE)
    await sio.enter_room(sid, user_room(user_id), namespace=SOCKETIO_NAMESPACE)


@sio.event(namespace=SOCKETIO_NAMESPACE)
async def disconnect(sid):
    return


@sio.event(namespace=SOCKETIO_NAMESPACE)
async def join_chat(sid, data):
    chat_id = (data or {}).get("chat_id")
    if not chat_id:
        return {"ok": False, "error": "chat_id required"}
    await sio.enter_room(sid, chat_room(chat_id), namespace=SOCKETIO_NAMESPACE)
    return {"ok": True}


@sio.event(namespace=SOCKETIO_NAMESPACE)
async def leave_chat(sid, data):
    chat_id = (data or {}).get("chat_id")
    if not chat_id:
        return {"ok": False, "error": "chat_id required"}
    await sio.leave_room(sid, chat_room(chat_id), namespace=SOCKETIO_NAMESPACE)
    return {"ok": True}


async def emit_message_to_chat(chat_id: str, payload: dict):
    await sio.emit("message:new", payload, room=chat_room(chat_id), namespace=SOCKETIO_NAMESPACE)


async def emit_message_to_user(user_id: str, payload: dict):
    await sio.emit("notify", payload, room=user_room(user_id), namespace=SOCKETIO_NAMESPACE)
