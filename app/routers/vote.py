#Routing for voting urls 
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

#Voting logic 
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    #See if user has voted
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, 
                                     models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1): 
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
            
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
        
    else: 
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
            
            vote_query.delete(sycnhronize_session = False)
            db.commit()
            
        return {"message": "successfully deleted vote"}
#need to set up schema