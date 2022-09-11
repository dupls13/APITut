from pydantic import BaseModel 

# Moved from main

# Define what a Post should look like
class Post(BaseModel):
    # User pydantic to see what type of data we want 
    # also restricts what will be sent (str, int...), validation
    title: str
    content: str
    # Defaults user entry
    published: bool = True
    # Allows user to add nothing 
    id : int 
    
class PostBase(BaseModel):
    title: str 
    content:str 
    published: bool = True
    id: int 

class PostCreate(PostBase):
    pass 

    
    