from fastapi import status,HTTPException,Depends,APIRouter
import models, schemas,database,oauth2
import routers
import sqlalchemy.ext.declarative
from sqlalchemy.orm import Session

from database import engine,get_db
from typing import List,Optional

router = APIRouter(
    prefix="/like",
    tags=['Like']

)

@router.post("/",status_code=status.HTTP_201_CREATED)       #as here is only / but it is actuall /like because like is prefix here 
def like(like: schemas.CreateLike, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)      #as in our schema we ar enot prviding user_id but we are going to take the user id form toke so why we using here current_user alot
    found_like = like_query.first()

    if(like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already liked the post {like.post_id} before this ")
        new_like = models.Like(post_id = like.post_id,user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully like dthe post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You can't unlike bcz u have never liked this post ")
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully unliked the post"}
