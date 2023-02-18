from sqlalchemy import DATETIME, Boolean, Column, Integer, String
from ....seedwork.infra.database import Base
import uuid
from sqlalchemy_utils import UUIDType


def generate_uuid():
    return str(uuid.uuid4())


class Products(Base):
    __tablename__ = "products"

    id = Column(String(36),
                primary_key=True, default=generate_uuid)
    product_name = Column(String, unique=True)
    product_version = Column(String, unique=True)
    deleted_at = Column(DATETIME, nullable=True)
