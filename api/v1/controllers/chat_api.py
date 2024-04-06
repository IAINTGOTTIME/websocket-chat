import os
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from chat_manager import ConnectionManager
from entities.message_entitie import Message
from services.massege_servise import  get_all_message
from db.engine import get_db

chat = APIRouter(prefix="/chat",
                 tags=["/chat"])

root = os.path.dirname("__file__")
with open(os.path.join(root, "chat.html"), "r") as file:
    html = file.read()

manager = ConnectionManager()


@chat.get("/")
def get_html():
    return HTMLResponse(html)


@chat.get("/message", response_model=List[Message])
def get_message(db: Session = Depends(get_db)):
    return get_all_message(db=db)


@chat.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,
                             client_id: int,
                             db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}",
                                    db=db, save=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat",
                                db=db, save=False)
