from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm       #by using this i will not be able to send login credential in body of postman buut  in form-data from postman
import models
import database
import schemas
import utils
import oauth2
from database import get_db
from sqlalchemy.orm import Session 

router = APIRouter(tags=['Authentication'])




# # def login(user_credentials : schemas.UserLogin, db: Session = Depends(database.get_db)):   #i will use if inot use authentication request form
# #     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()


@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()     #in request form there 1sr attribute is username which may be suername or email
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"Invalid Credentials")
    
    #here the 1st password is from requestside and the 2nd is form db which was stored in hashed formate
    if not utils.verify(user_credentials.password, user.password):  
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"Invalid Credentials")
    

    # crate a token
    # return a JWt token

    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}



# Logout endpoint
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
token: str = Depends(oauth2.oauth2_scheme)  # Extract token
):
    # **ADD TOKEN TO BLACKLIST**
    oauth2.TOKEN_BLACKLIST.add(token)
    

    return {"message": "Successfully logged out"}
