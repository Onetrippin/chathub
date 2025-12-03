import asyncio
import websockets
from fastapi import WebSocket
from config import MESSAGE_URL


def _http_to_ws(url: str) -> str:
    if url.startswith("https://"):
        return "wss://" + url[len("https://"):]
    if url.startswith("http://"):
        return "ws://" + url[len("http://"):]
    return url


async def ws_proxy(client_ws: WebSocket, chat_id: str, user_id: str):
    await client_ws.accept()

    backend_base = _http_to_ws(MESSAGE_URL)
    backend_url = f"{backend_base}/ws/chat/{chat_id}?user_id={user_id}"

    async with websockets.connect(backend_url) as backend_ws:

        async def client_to_backend():
            try:
                while True:
                    msg = await client_ws.receive_text()
                    await backend_ws.send(msg)
            except Exception:
                await backend_ws.close()

        async def backend_to_client():
            try:
                while True:
                    msg = await backend_ws.recv()
                    await client_ws.send_text(msg)
            except Exception:
                await client_ws.close()

        await asyncio.gather(client_to_backend(), backend_to_client())
