from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.schemas import UserCreate, UserResponse
from app import models
from sqlalchemy.orm import Session
from app.utils import hash
from app.database import engine, get_db

router = APIRouter(
    prefix= "/user",
    tags=['User']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    user.password = hash(user.password)

    new_user = models.User(**user.dict())

    # new_post = models.Post(title = post.title, content = post.content , published = post.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist.!")

    return user
