from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ...modules.ticket.domain.entities import Base
from ...seedwork.infra.database import SessionLocal, engine
from ...modules.ticket.domain.entities import Tickets
from ...modules.user.domain.entities import Users
from ..models import CreateTickets
from ...seedwork.utils.functional import create_status, get_user_exception, update_status
from .users import get_current_user


Base.metadata.create_all(bind=engine)

app = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/ticket")
def create_new_ticket(create_ticket: CreateTickets, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):

    if user["role"] != "user":
        raise get_user_exception()

    create_ticket_model = Tickets()
    cs = db.query(Users).filter(
        Users.role == "cs").order_by(func.random()).first()

    if cs is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No CS for now")

    create_ticket_model.title = create_ticket.title
    create_ticket_model.problem = create_ticket.problem
    create_ticket_model.product_name = create_ticket.product_name
    create_ticket_model.product_version = create_ticket.product_version
    create_ticket_model.creator_id = user["id"]
    create_ticket_model.cs_id = cs.id

    db.add(create_ticket_model)
    db.commit()

    return create_status("Ticket created!")


@app.post("/ticket/close/{ticket_id}")
def close_ticket(ticket_id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    if user["role"] != "cs":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only CS that permitted to close this ticket!")

    ticket_model = db.query(Tickets).filter(Tickets.id == ticket_id).first()

    if ticket_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There's no ticket with that ID")

    if ticket_model.status == "close":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This ticket already closed")

    ticket_model.status = "close"
    db.commit()
    return update_status("Ticket sucessfully closed!")


@app.post("/ticket/pass/")
def pass_ticket_to_other_cs(ticket_id: str, cs_id: str, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    if user["role"] != "cs":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only CS that permitted to pass this ticket!")

    ticket_model = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    cs_model = db.query(Users).filter(Users.id == cs_id).first()

    if cs_model is None or cs_model.role != "cs":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No CS Found")
    if cs_model.id == user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You cannot pass this ticket to yourself!")
    if ticket_model.id != user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not permitted to pass this ticket!")
    if ticket_model.status == "close":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"This ticket closed, why you want to pass it?")

    ticket_model.cs_id = cs_model.id
    db.commit()

    return update_status("Success passing ticket!")
