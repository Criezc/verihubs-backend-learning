from ...modules.user.domain.entities import Users
from passlib.context import CryptContext
from fastapi import status, HTTPException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hashed(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def auth_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).filter(
        Users.deleted_at == None).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Exceptions


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials!",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response


def create_status(detail: str):
    create_response = HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=detail,
    )
    return create_response


def update_status(detail: str):
    create_status = HTTPException(
        status_code=status.HTTP_200_OK,
        detail=detail
    )
    return create_status
