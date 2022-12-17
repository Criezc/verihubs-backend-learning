from fastapi import FastAPI, HTTPException
from typing import List
from src.domain.User.models import User, Gender, Role, UserUpdateRequest
from uuid import UUID, uuid4

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.admin]
    ),
    User(
        id=uuid4(),
        first_name="Alex",
        last_name="John",
        gender=Gender.male,
        roles=[Role.user, Role.admin]
    )
]


@app.get("/")
async def root():
    return {"Hello": "Frisco"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/register")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.post("/api/v1/login")
async def login_user():
    return


@app.get("/api/v1/unprotected")
async def unprotected_login():
    return {
        "Hello": "World"
    }


@app.get("/api/v1/protected")
async def protected_login():
    return {}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )
