from datetime import datetime
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...seedwork.infra.database import SessionLocal, engine
from ...modules.user.domain.entities import Base
from ...modules.product.domain.entities import Products
from ..models import CreateProducts
from ...seedwork.utils.functional import create_status, update_status


Base.metadata.create_all(bind=engine)

app = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/product/create_product")
def create_new_product(create_prod: CreateProducts, db: Session = Depends(get_db)):
    try:
        create_product_model = Products()
        create_product_model.product_name = create_prod.product_name
        create_product_model.product_version = create_prod.product_version
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    db.add(create_product_model)
    db.commit()
    return create_status("Product created!")


@app.put("/product/{product_id}")
def update_product(product_id: str, create_prod: CreateProducts, db: Session = Depends(get_db)):
    product_model = db.query(Products).filter(
        Products.id == product_id).first()

    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    product_model.product_name = create_prod.product_name
    product_model.product_version = create_prod.product_version

    db.add(product_model)
    db.commit()

    return update_status("Product updated!")


@app.delete("/product/")
def delete_product(product_name: Optional[str] = None, product_version: Optional[str] = None, db: Session = Depends(get_db)):

    if product_version:
        db.query(Products).filter(Products.product_version == product_version).filter(Products.deleted_at == None).update({
            "deleted_at": datetime.utcnow()
        })
        db.commit()
    else:
        db.query(Products).filter(Products.deleted_at == None).filter(Products.product_name == product_name).update({
            "deleted_at": datetime.utcnow()
        })
        db.commit()

    return update_status("Delete success!")


@app.get("/product/")
def read_all_product(prod_name: Optional[str] = None, prod_version: Optional[str] = None, db: Session = Depends(get_db)):

    if prod_name:
        prod_model = db.query(Products).filter(
            Products.product_name == prod_name).filter(Products.deleted_at == None).first()
        if prod_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        else:
            return prod_model
    if prod_version:
        prod_model = db.query(Products).filter(
            Products.product_version == prod_version).filter(Products.deleted_at == None).first()
        if prod_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db.query(Products).filter(Products.deleted_at == None).all()
