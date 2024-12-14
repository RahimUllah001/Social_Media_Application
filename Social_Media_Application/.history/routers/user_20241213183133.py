from fastapi import status,HTTPException,Depends,APIRouter
import utils        # utils is the file name in same folder and i want to acces their intances 
import schemas      #this are the file names in the same folder
import models
from sqlalchemy.orm import Session
from database import get_db
from pydantic import EmailStr
import oauth2

import secrets
from datetime import datetime, timedelta
from utils import send_email
from models import Follow


router = APIRouter(
    prefix="/users",
    tags=['Users']

)

# Creating user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db:Session = Depends(get_db)): 

    # hash the password - user.password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Follow a user
@router.post("/follow", response_model=schemas.FollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(request: schemas.FollowRequest, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    if not request.followee_id:
        return {"message":"user with this id not exists"}
    if current_user.id == request.followee_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")

    # Check if already following
    existing_follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followee_id == request.followee_id
    ).first()

    if existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")

    follow = Follow(follower_id=current_user.id, followee_id=request.followee_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

# Unfollow a user
@router.delete("/unfollow/{followee_id}", status_code=status.HTTP_200_OK)
def unfollow_user(followee_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followee_id == followee_id
    ).first()

    if not follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow relationship not found")

    db.delete(follow)
    db.commit()
    return {"message":"Successfully unfollowed"}



# Get profile with followers and following count
@router.get("/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    followers_count = db.query(Follow).filter(Follow.followee_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()

    return {
        "id": user.id,
        "email": user.email,
        "followers_count": followers_count,
        "following_count": following_count
    }



# For get password and this will call reset password function





@router.post("/forget_password/", status_code=status.HTTP_200_OK)
def forget_password(user_email: str, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")

    # Generate reset token and expiry time
    reset_token = secrets.token_hex(32)  # Secure random token
    token_expiry = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 minutes

    # Update user with reset token and expiry
    user.reset_token = reset_token
    user.reset_token_expiry = token_expiry
    db.commit()

    # Email the reset token to the user
    reset_link = f"http://127.0.0.1:8000/users/reset_password/?token={reset_token}"
    email_subject = "Password Reset Request"
    email_body = f"Click on the following link to reset your password: {reset_link}\n\nIf you did not request this, please ignore this email."

    send_email(email_subject, email_body, user_email)

    return {"message": "Password reset link sent to your email"}






@router.post("/reset_password/", status_code=status.HTTP_200_OK)
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # Validate the token
    user = db.query(models.User).filter(models.User.reset_token == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    # Check if the token is expired
    if user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")

    # Hash the new password
    hashed_password = utils.hash(new_password)

    # Update user's password and clear the token
    user.password = hashed_password
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()

    return {"message": "Password reset successful"}

