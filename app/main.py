from app.routers import post, user
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app import models
from fastapi.params import Body
from random import randint
import psycopg2 as psc
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app.database import engine, get_db
import app.models
app.models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psc.connect(host="localhost", database="fastapi", user="postgres",
                           password="tahanaviwala123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected Successfully.!")
        break

    except Exception as error:
        print("Connection error" + str(error))
        time.sleep(2)

my_posts = [{"title": "post 1", "content": "content of post 1", "id": 1}, {
    "title": "fruits", "content": "Apple Mango", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "welcome to my api"}
