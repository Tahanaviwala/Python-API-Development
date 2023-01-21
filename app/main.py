from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randint
import psycopg2 as psc
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.schemas import Post, PostCreate, PostResponse, UserCreate, UserResponse
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


@app.get("/")
def root():
    return {"message": "welcome to my api"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * from posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/createposts", status_code=status.HTTP_201_CREATED , response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    # new_post = models.Post(title = post.title, content = post.content , published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@app.get("/posts/{id}" , response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found.!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.!")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.!")
        
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()


    update_post = db.query(models.Post).filter(models.Post.id == id)
    get_post = update_post.first()
    

    if get_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.!")
        
    update_post.update(post.dict(),synchronize_session=False)
    db.commit()

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    return update_post.first()



@app.post("/createuser", status_code=status.HTTP_201_CREATED , response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    # new_post = models.Post(title = post.title, content = post.content , published = post.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
