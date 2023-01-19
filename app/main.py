from sqlalchemy.orm import Session
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import psycopg2 as psc
from psycopg2.extras import RealDictCursor
import time

from app.database import engine, get_db
import app.models
from app.models import Post
app.models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "welcome to my api"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * from posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id))
    post = cursor.fetchone()
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found.!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.!")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.!")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    cursor.execute("UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.!")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    return {'data': updated_post}
