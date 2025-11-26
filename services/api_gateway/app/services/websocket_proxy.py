import websockets
import asyncio
from config import MESSAGE_URL


async def ws_proxy(client_ws, chat_id: str, user_id: str):
    await client_ws.accept()

    url = f'{MESSAGE_URL.replace('http', 'ws')}/ws/chat/{chat_id}?user_id={user_id}'

    async with websockets.connect(url) as backend_ws:

        async def client_to_backend():
            try:
                while True:
                    msg = await client_ws.receive_text()
                    await backend_ws.send(msg)
            except:
                await backend_ws.close()

        async def backend_to_client():
            try:
                while True:
                    msg = await backend_ws.recv()
                    await client_ws.send_text(msg)
            except:
                await client_ws.close()

        await asyncio.gather(client_to_backend(), backend_to_client())
