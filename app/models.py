from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text 
from .database import Base 
from sqlalchemy.orm import relationship 
# used to connect to DB


#Limitation of sqlalchemy: If updating table with new column, new column will not show up unless drop table first 
#Need to add database migration tool 

#Defines what table will look like 
# Create class for posts, extends to base 
class Post(Base):
    # Make name for table
    __tablename__ = "posts"
    #Add columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))
    #Make foreign key with user (Doesn't update old table)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    #contraint of SQLalchemy: doesn't help modify tables 
    
    
    #Create relationship (creates new property to return User)
    owner = relationship("User")
    
    """Schema/pydantic models define the structure of a request and response 
    ensure that when a use want to create a post, the request will only go through 
    if it has a title and content in body"""
    #models here are sqlalchemy, not schema 
    """ sqlalchemy (ORM) model responsible for defining the columns of our posts table 
    within postgres
    used to query, create, delete, and update entries within database"""
    
class User(Base): 
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable = False, unique=True) 
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))
    
#Creates table for voting database 
class Votes(Base): 
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)