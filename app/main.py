import pwd
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel 
#from passlib.context import CryptContext
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

from .routers import posts, users, auth

app = FastAPI()

#Hashing for paswords
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#connect model
models.Base.metadata.create_all(bind=engine)
# After engine added, need to change path operation functions

# Create dependency for model , Gets session for db, talk to it 
"""def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()"""
        # Moved to database.py

# Define what a Post should look like
"""class Post(BaseModel):
    # User pydantic to see what type of data we want 
    # also restricts what will be sent (str, int...), validation
    title: str
    content: str
    # Defaults user entry
    published: bool = True
    # Allows user to add nothing 
    id = int """

# Code to connect to database 
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

#Create open dictionary to grab
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 1},
            {"title":"favorite foods", "content": "I like pizza", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i 


# moved paths to routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


#Decorator: converts to path operation in FastAPI
# TODO: Check out HTTP Methods
# @app : Decorator get: HTTP Method / : Path 
@app.get('/')
#Function
def root():
    #Data that gets sent back to user 
    #converts to JSON
    return {'message': 'Welcome to my API!!!'}




