from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import submit

app = FastAPI(title="CodeSage API", description="A LeetCode-inspired clone with an AI guide.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submit.router, prefix="/api")


@app.get("/")
async def root():
    return {"name": "CodeSage API", "docs": "/docs", "api_prefix": "/api"}
