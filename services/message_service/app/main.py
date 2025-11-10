from fastapi import FastAPI, WebSocket

app = FastAPI(title='Message Service')


@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text('connected')
