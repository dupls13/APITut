from fastapi import APIRouter, Depends, status, HTTPException, Response 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

#Check to see if username and password are correct 
#Change to Oauth, token allows retrieval from API
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    
    
    #Grab user, filter by email, only grab first (since only one email )
    #With Oath, only returning username, password, but not located, so need to change
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    #If there are no users by that email 
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #Have to check if password is correct
    #Seen in utils, verify if password matches 
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Creates token for user 
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    
    #created token 
    #return token 
    return {"access_token" : access_token, "token_type": "bearer"}