from sqlalchemy.orm import Session
from db.models.massage_model import MessageOrm


def add_message_db(message: str, db: Session):
    new_message = MessageOrm(message=message)
    db.add(new_message)
    db.commit()
    return


def get_all_message(db: Session):
    all_messages = db.query(MessageOrm).order_by(MessageOrm.id).all()
    return all_messages

