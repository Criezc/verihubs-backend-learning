from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from seedwork.infra.database import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    product_version = Column(String)
