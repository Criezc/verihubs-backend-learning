from fastapi import FastAPI
from .routers import users, products, tickets

app = FastAPI()
app.include_router(users.app)
app.include_router(products.app)
app.include_router(tickets.app)


@app.get("/")
async def root():
    return {
        "message": "DB initialized"
    }
