
from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint 
# Base class or base model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool =True 



# request type for user creation
class CreateUser(BaseModel):
    email: EmailStr
    password: str

# Response on user creation 
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# model for creating post how type data it should expct whne creating a post  
class CreatePost(PostBase):
    image_url: str
    pass

# model for updating post how type data it should expct whne updating a post  

class UpdatePost(PostBase):
    pass

# what type of data it will giv ein repsonse
class PostResponse(PostBase):
    
    id: int 
    created_at: datetime
    owner_id: int       #this will show whime created the post
    owner : UserResponse                                        #this line means that owner attribute is eaual to usreresponse which is actually reponse on user creation it will reutrn id,email and cratedat time
    
    # As sqlachemy return an objects but pydantic can only work with dictionary so the bewlow two line wil make pydantic able to work with objet of orm/sqlalchemy 
    class Config:
        orm_mode = True
            #model_config = ConfigDict(from_attributes=True)        #in pydantic version we have to write this intead of writng the above two lines

# this response is for when i am getting all posts it will give these follwoing data
class PostWithLike(BaseModel):
    post: PostResponse
    likes:int
    class Config:
        orm_mode = True




# request type for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str 

# Response to login as it give a token in return Token in response
class Token(BaseModel):
    access_token: str 
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    # create_at: datetime


#when we are going to make like what  type of data the like function should expect or what data we should send
class CreateLike(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)    #dir mean direcion as we can like or want to remove our like form post  so we will use dir= 1 for likeness and dir=0 for removing our like