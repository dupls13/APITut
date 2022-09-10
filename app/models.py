from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text 
from .database import Base 
# used to connect to DB

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
    
    #contraint of SQLalchemy: doesn't help modify tables 