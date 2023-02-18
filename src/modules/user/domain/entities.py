from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from ....seedwork.infra.database import Base

import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Users(Base):
    __tablename__ = "users"

    id = Column(String(36),
                primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    deleted_at = Column(DATETIME, nullable=True)
