from sqlalchemy.orm import Session
from db.models.massage_model import MessageOrm


def add_message_db(message: str, db: Session):
    new_message = MessageOrm(message=message)
    db.add(new_message)
    db.commit()
    return
