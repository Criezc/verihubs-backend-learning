from fastapi import FastAPI
from .routers import users

app = FastAPI()
app.include_router(users.app)


@app.get("/")
async def root():
    return {
        "message": "DB initialized"
    }
