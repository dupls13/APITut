from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from typing import List, Optional
from ..database import get_db 
from .. import models, schemas, oauth2


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


#Added requirement for confirming user is logged in 
# Added user limit to recieving certain number of posts 
# Added skip option

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # Getting posts from DB
    #posts = cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #if only want posts that belong to specific user, rather than all posts ever
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# defining dictionary to be sent #New function is dependency, user must be logged in to create post 
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    # SQL connection to creating posts 
    # %s prevent SQL injections, they are just placeholders, values are put in after 
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * 
                  # """, (post.title, post.content, post.published))
    #Need to make different variable for above
    #new_post = cursor.fetchone()
    # Need to commit to table 
    #conn.commit()
    
    
    #After adding foreign key, need to automatically get user when creating new post 
    #owner_user.id
    
    # Add ** to fill in fields automatically (title, content, etc)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    # What do we want inside the post: title, content (str)
    
    
# Get the post you want
# id is path parameter, links to specific post 
@router.get("/{id}", response_model=schemas.Post)    
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # logic for deleting post 
    # find the index in the array that has required ID
    # my_posts.pop(index)
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
   #deleted_post = cursor.fetchone()
    #conn.commit()
    
    # Grabs query 
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    
    # Check if post is owners 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized for action.")
    
    #deletes post 
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
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
