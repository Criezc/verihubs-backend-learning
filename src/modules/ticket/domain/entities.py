from sqlalchemy import Column, Integer, String, Enum
from ....seedwork.infra.database import Base
import uuid
from sqlalchemy_utils import UUIDType


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    problem = Column(String)
    product_name = Column(String)
    product_version = Column(String)
    cs_id = Column(UUIDType(binary=False))
    creator_id = Column(UUIDType(binary=False))
    status = Column(Enum("open", "close"), default="open")
