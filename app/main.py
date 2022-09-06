from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel 
from typing import Optional
from random import randrange

app = FastAPI()

# Define what a Post should look like
class Post(BaseModel):
    # User pydantic to see what type of data we want 
    # also restricts what will be sent (str, int...), validation
    title: str
    content: str
    # Defaults user entry
    published: bool = True
    # Allows user to add nothing 
    rating: Optional[int] = None

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
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# defining dictionary to be sent
def create_posts(post:Post):   
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000) 
    my_posts.append(post_dict)
    return {"data": post_dict}
    # What do we want inside the post: title, content (str)
    
@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

# Get the post you want
# id is path parameter, links to specific post 
@app.get("/posts/{id}")    
def get_post(id: int, response: Response):
    post = find_post(id)
    
    #Gives error when post id not found (not created)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'post with id {id} was not found'}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ):
    # logic for deleting post 
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    
    # wants to update, this checks to see if id exists
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')

    #if does, take all data received from front, converts to dict
    post_dict = post.dict()
    # Add id
    post_dict['id'] = id
    
    # replaces dict with given id 
    my_posts[index] = post_dict
    return {"data": post_dict}
