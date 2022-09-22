from base64 import encode
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 


#Endpoint of login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#3 pieces of information for token 
# Secret key 
#Algorithm used 
#Expiration time of token 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
   to_encode = data.copy()
   
   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({'exp': expire})
   
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   
   return encoded_jwt

#Get data
def verify_access_token(token: str, credentials_exception):
    
    try:
        #Decode jwt token 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #Extract id 
        id: str = payload.get("user_id")
        
        #Validates token schema
        if id is None: 
            raise credentials_exception
        #Return token data
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

#Pass dependency, takes token automatically, makes sure correct, then extract id ,user

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    #When credentials are wrong 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f'Could not validate credentials', 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    
    
    return user