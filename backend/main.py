from fastapi import FastAPI
from routers import submit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(submit.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
