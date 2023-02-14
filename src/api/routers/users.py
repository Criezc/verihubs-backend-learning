from fastapi import APIRouter, Depends, HTTPException, status

from ...seedwork.utils.functional import get_password_hashed
from ...seedwork.infra.database import SessionLocal, engine
from ...modules.user.domain.entities import Base
from ..models import CreateUser
from sqlalchemy.orm import Session
from ...modules.user.domain.entities import Users


Base.metadata.create_all(bind=engine)

app = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/user/create_user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users()
    create_user_model.username = create_user.username
    create_user_model.role = create_user.role
    hash_password = get_password_hashed(create_user.password)
    create_user_model.hashed_password = hash_password

    db.add(create_user_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
