from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import uuid
from datetime import datetime, timedelta
#
from ...seedwork.utils.functional import get_password_hashed, get_user_exception, create_status, token_exception, auth_user
from ...seedwork.infra.database import SessionLocal, engine
from ...modules.user.domain.entities import Base
from ..models import CreateUser
from ...modules.user.domain.entities import Users

SECRET_KEY = "C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdS"
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    encode = {
        "sub": username,
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("sub")

        if username is None:
            raise get_user_exception()
        return {"username": username}
    except JWTError:
        raise get_user_exception()


@app.post("/user/create_user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users()
    create_user_model.username = create_user.username
    create_user_model.role = create_user.role
    hash_password = get_password_hashed(create_user.password)
    create_user_model.hashed_password = hash_password

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
        user.username, expires_delta=token_expire
    )
    return {
        "token": token
    }


@app.get("/user/")
async def get_all_user(db: Session = Depends(get_db), user_role: Optional[str] = None):

    if user_role:
        user_model = db.query(Users).filter(Users.role == user_role).all()
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            return user_model
    else:
        return db.query(Users).all()


@app.put("/user/{user_id}")
async def update_user(user_id: str, users: CreateUser,  db: Session = Depends(get_db)):
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

    return create_status("Update success!")


@app.delete("/user/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_model = db.query(Users).filter(Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()

    return create_status("Delete success!")
