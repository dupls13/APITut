from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time 
from .config import settings 

# Need to connect a database 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


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

#Moved from main.py 
# Code to connect to database 
"""
while True:
    try:
        # Hard coded in, future needs changes
        conn = psycopg2.connect(host='localhost', database='fastapi', 
                                user='postgres', password='3875',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
        
"""