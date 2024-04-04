from fastapi import APIRouter
from .controllers.chat_api import chat

router = APIRouter(prefix="/v1")
router.include_router(chat)
