from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Need to connect a database 
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:3875@localhost/fastapi'


# Create engine , established connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Need to make session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()


