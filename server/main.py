from api.endpoints import chat_router
from fastapi import FastAPI

app = FastAPI(
    description="ReWOO + Human in the loop",
    version="0.0.1",
)

app.include_router(prefix="/v1", router=chat_router)
