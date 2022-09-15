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

#Decorator: converts to path operation in FastAPI
# TODO: Check out HTTP Methods
# @app : Decorator get: HTTP Method / : Path 
@app.get('/')
#Function
def root():
    #Data that gets sent back to user 
    #converts to JSON
    return {'message': 'Welcome to my API!!!'}

# request Get methods url: "/posts"
#List allows getting all posts, since others are used to only recieving one 
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # Getting posts from DB
    #posts = cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# defining dictionary to be sent
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):  
    # SQL connection to creating posts 
    # %s prevent SQL injections, they are just placeholders, values are put in after 
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * 
                  # """, (post.title, post.content, post.published))
    #Need to make different variable for above
    #new_post = cursor.fetchone()
    # Need to commit to table 
    #conn.commit()
    
    # Add ** to fill in fields automatically (title, content, etc)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    # What do we want inside the post: title, content (str)
    
@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

# Get the post you want
# id is path parameter, links to specific post 
@app.get("/posts/{id}", response_model=schemas.Post)    
def get_post(id: int, db: Session = Depends(get_db)):
    #Fetching specific post. Need to convert int back to string , sometimes need extra comma 
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    #Gives error when post id not found (not created)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'post with id {id} was not found'}
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    # logic for deleting post 
    # find the index in the array that has required ID
    # my_posts.pop(index)
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
   #deleted_post = cursor.fetchone()
    #conn.commit()
    
    # Grabs query 
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    
    #deletes post 
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db)):
 #   cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
  #                 (post.title, post.content, post.published, str(id),))
    
 #   updated_post = cursor.fetchone()
 #   conn.commit()
 #   print(post)
    
    # wants to update, this checks to see if id exists
    #index = find_index_post(id)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')

    #Update query. can hard code title, content 
    #post_query.update({'title': 'hey this is my updated title',
                    #   'content': 'this is my updated content'}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    #if does, take all data received from front, converts to dict
    #post_dict = post.dict()
    # Add id
    #post_dict['id'] = id
    
    # replaces dict with given id 
    #my_posts[index] = post_dict
    return post_query.first()

"""
#Test
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    #Make a query
    
    #This replaces SQL statements 
    posts = db.query(models.Post).all()
    
    return {"datas": posts}
    """
    

#Practice with postgres and SQL



# Create users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Create hash of password - user.password 
    #hashed_password =pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user