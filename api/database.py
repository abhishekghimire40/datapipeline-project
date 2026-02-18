from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import config

# creating connection to our database
engine = create_engine(config.SQLALCHEMY_DATABASE_URL)
# creates session for each database query or operation
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db
