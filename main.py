import os
import uvicorn
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from api.db.database import create_database
from api.db.mongo import create_nosql_db
from api.v1.routes.auth import app as auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    create_nosql_db()
    yield
    ## write shutdown logic below yield

app = FastAPI(lifespan=lifespan)

create_nosql_db()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://hng-st-three-project.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, tags=["Auth"])
# app.include_router(users, tags=["Users"])

@app.get("/", tags=["Home"])
async def get_root(request: Request) -> dict:
    return {
        "message": "Welcome to API",
        "URL": "",
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)