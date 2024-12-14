from fastapi import FastAPI
from database import engine
from routers import post, user,auth,like
import models
from config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) as now i use alembic  for db not sqlalachemy directly


app = FastAPI()

# origins = ["https://www.google.com","https://www.youtube.com"]        #to allow only tour specifies origins or to rpvide strict origins
origins = ["*"]     #to all laow alltypes of frotn end origin who can access your bacjened  or all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],        #this line means which tyoe i method i can alow that what t ype of requests poeole can do e.g post or get or wthey will be allowed to do delete or update
    allow_headers=["*"],        
)


# this three lines show the path appication ==>  Api Router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


