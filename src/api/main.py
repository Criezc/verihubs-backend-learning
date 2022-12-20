from fastapi import Body, Depends, FastAPI, HTTPException
from typing import List
from src.domain.User.models import User, Gender, Role, UserUpdateRequest
from uuid import UUID, uuid4
from ..domain.User.schemas import UserEntity, UserLoginEntity
from .auth.auth import signJWT
from .auth.bearer import jwtBearer


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

users = []


@app.get("/")
async def root():
    return {"Hello": "Frisco"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.get("/api/v1/unprotected")
async def unprotected_login():
    return {
        "Hello": "World"
    }


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


@app.post("/api/v1/user/signup", tags=["user"], status_code=201)
def user_signup(user: UserEntity = Body(default=None)):
    users.append(user)
    return signJWT(user.username)


def check_user(data: UserEntity):
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
        return False


@app.post("/api/v1/user/login", tags=["user"])
def user_login(user: UserLoginEntity = Body(default=None)):
    if check_user(user):
        return signJWT(user.username)
    else:
        raise HTTPException(
            status_code=404,
            detail="Invalid login details!"
        )
