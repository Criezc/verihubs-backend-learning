from sqlalchemy import Column, Integer, String, ForeignKey
from ....seedwork.infra.database import Base
from sqlalchemy_utils import UUIDType
import uuid


class Users(Base):
    __tablename__ = "users"

    id = Column(UUIDType(binary=False),
                primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
