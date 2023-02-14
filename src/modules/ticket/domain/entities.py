from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from seedwork.infra.database import Base


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    problem = Column(String)
    product_name = Column(String)
    product_version = Column(String)
