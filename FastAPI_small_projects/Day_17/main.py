# Websocket notifications

from fastapi import FastAPI
from fastapi import WebSocket
from pydantic import BaseModel

app = FastAPI()
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            await websocket.send_text(
                f"You sent: {data}"
            )
    except:
        active_connections.remove(websocket)

class Notification(BaseModel):
    message: str


@app.post("/notify")
async def notify(notification:Notification):

    for connection in active_connections:
        await connection.send_text(
            notification.message
        )

    return {
        "status": "sent"
    }