from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import chat_router

app = FastAPI(
    description="ReWOO + Human in the loop",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefix="/v1", router=chat_router)
