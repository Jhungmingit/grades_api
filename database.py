import os                            # Lets you read environment variables 
from dotenv import load_dotenv       # reads the .env file and loads its lines into the environment
from sqlalchemy import create_engine # builds the object that talks to PostgreSQL
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session # creates the parent class for the ORM models
# session maker builds the factory that produces sessions, session is only used as a type hint, so the editor knows what get_db yields 
from collections.abc import Generator # is only a type hint, describing a function that uses yield
# A yield is like a return function but pauses it instead of finishing

load_dotenv() # opens .env and copies DATABASE_URL= 

DATABASE_URL = os.environ["DATABASE_URL"] # here we use [...] brackets instead of get() which is good for this situation because it crashes immediatly if the variable is missing
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


SessionLocal = sessionmaker(
    autoflush=False,                   # sqlalchemy wont automatically send pending changes 
    bind=engine,                       # which database this session talks to
)

class Base(DeclarativeBase):
    pass 

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()