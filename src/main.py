from fastapi import Depends, FastAPI, HTTPException
from typing import List
from src.domain.User.models import User, Gender, Role, UserUpdateRequest
from uuid import UUID, uuid4
from .auth import AuthHandler
from .domain.User.schemas import AuthDetails

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

auth_handler = AuthHandler()

users = []


@app.get("/")
async def root():
    return {"Hello": "Frisco"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/register", status_code=201)
async def register_user(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username already taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return


@app.post("/api/v1/login")
async def login_user(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(
            status_code=401,
            detail="Invalid username and/or password"
        )
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@app.get("/api/v1/unprotected")
async def unprotected_login():
    return {
        "Hello": "World"
    }


@app.get("/api/v1/protected")
async def protected_login(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}


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
