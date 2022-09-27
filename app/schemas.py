from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Moved from main

# Define what a Post should look like
"""class Post(BaseModel):
    # User pydantic to see what type of data we want 
    # also restricts what will be sent (str, int...), validation
    title: str
    content: str
    # Defaults user entry
    published: bool = True
    # Allows user to add nothing 
    id : int """
    
class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True 
    
class PostCreate(PostBase):
    pass 
    

    
#User class 
class UserCreate(BaseModel):
    email : EmailStr
    password : str 
    
class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime 
    
    class Config: 
        orm_mode = True

class UserLogin(BaseModel): 
    email: EmailStr
    password: str 
    

class Token(BaseModel):
    access_token: str 
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None 
    
    

# Class for sending response back to user 
#Setup up to also return owner information from post 
class Post(PostBase):
    id:int
    created_at: datetime
    #Get user id 
    owner_id: int 
    owner: UserOut
    
    
    #Need to add this after adding to path response_model
    #pydantic has to change from sqlalchemy model back to pydantic model
    #when returning back to user 
    class Config: 
        orm_mode = True
    