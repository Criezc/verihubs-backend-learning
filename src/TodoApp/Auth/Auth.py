from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from ..Models.models import Users, Base
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..Db.Database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..Utils.utils import auth_user, get_password_hashed
from datetime import datetime, timedelta
from jose import jwt, JWTError


SECRET_KEY = "C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdS"
ALGORITHM = "HS256"


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


Base.metadata.create_all(bind=engine)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
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
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_password = create_user.password

    hash_password = get_password_hashed(create_user.password)

    create_user_model.hashed_password = hash_password

    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()
    return successful_response(201)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_user(form_data.username, form_data.password, db)

    if not user:
        raise token_exception()
    token_expire = timedelta(minutes=20)
    token = create_access_token(
        user.username, user.id, expires_delta=token_expire)
    return {
        "token": token
    }

# Exeptions


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")
