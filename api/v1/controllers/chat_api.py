import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from db.models.massage_model import MessageOrm
from services.massege_servise import add_message_db

from db.engine import get_db

chat = APIRouter(prefix="/chat",
                 tags=["/chat"])

root = os.path.dirname("__file__")
with open(os.path.join(root, "chat.html"), "r") as file:
    html = file.read()


@chat.get("/")
def get_html():
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, db: Session):
        add_message_db(message=message, db=db)
        for connection in self.active_connections:
            await connection.send_text(message)

    # @staticmethod
    # def add_message_db(message: str, db: Session):
    #     new_message = MessageOrm(message=message)
    #     db.add(new_message)
    #     db.commit()
    #     return


manager = ConnectionManager()


@chat.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,
                             client_id: int,
                             db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", db=db)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", db=db)
