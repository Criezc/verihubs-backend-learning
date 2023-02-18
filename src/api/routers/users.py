from typing import Optional, Dict
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
#
from ...seedwork.utils.functional import get_password_hashed, get_user_exception, create_status, token_exception, auth_user, update_status
from ...seedwork.infra.database import SessionLocal, engine
from ...modules.user.domain.entities import Base
from ..models import CreateUser, UpdateUser
from ...modules.user.domain.entities import Users

SECRET_KEY = "C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdS"
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/login")

app = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(username: str, user_id: str, user_role: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id, "role": user_role}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise get_user_exception()


@app.post("/user/create_user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users()
    create_user_model.username = create_user.username
    create_user_model.role = create_user.role
    hash_password = get_password_hashed(create_user.password)
    create_user_model.hashed_password = hash_password
    create_user_model.deleted_at = None

    db.add(create_user_model)
    db.commit()

    return create_status("User created!")


@app.post("/user/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_user(form_data.username, form_data.password, db)

    if not user:
        raise token_exception()
    token_expire = timedelta(minutes=20)
    token = create_access_token(
        user.username, user.id, user.role, expires_delta=token_expire)
    return {
        "access_token": token
    }


@app.get("/user/")
async def get_all_user(db: Session = Depends(get_db), user_role: Optional[str] = None):

    if user_role:
        user_model = db.query(Users).filter(
            Users.role == user_role).filter(Users.deleted_at == None).all()
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            return user_model
    else:
        return db.query(Users).filter(Users.deleted_at == None).all()


@app.put("/user/{user_id}")
async def update_user(user_id: str, users: UpdateUser,  db: Session = Depends(get_db)):
    user_model = db.query(Users).filter(
        Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user_model.username = users.username
    user_model.role = users.role
    hash_password = get_password_hashed(users.password)
    user_model.hashed_password = hash_password

    db.add(user_model)
    db.commit()

    return update_status("Update success!")


@app.delete("/user/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_model = db.query(Users).filter(Users.id == user_id).filter(
        Users.deleted_at == None).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.query(Users).filter(Users.id == user_id).update({
        "deleted_at": datetime.utcnow()
    })
    db.commit()

    return update_status("Delete success!")
