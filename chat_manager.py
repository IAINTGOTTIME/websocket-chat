from sqlalchemy.orm import Session
from starlette.websockets import WebSocket
from services.massege_servise import add_message_db


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, save: bool, db: Session):
        if save:
            add_message_db(message=message, db=db)
        for connection in self.active_connections:
            await connection.send_text(message)
