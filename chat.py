from fastapi import FastAPI
from api.v1 import router

app = FastAPI(title="Chat")
app.include_router(router)
