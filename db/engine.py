from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    url=f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

session = sessionmaker(engine, expire_on_commit=False)


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()
