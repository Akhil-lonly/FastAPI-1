import os
from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import schemas, database, models
from hashing import Hash

SessionLocal = database.SessionLocal
engine = database.engine

models.Base.metadata.create_all(engine)

app = FastAPI()
User = schemas.User


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get a user with requested email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# save profile picture into a directory 'profile/user_id'
def save_profile_picture(picture: UploadFile, user_id: int):
    path = f"profiles/{user_id}/{picture.filename}"
    if not os.path.exists(f"profiles/{user_id}"):
        os.mkdir(f"profiles/{user_id}")
    picture.save(path)
    return path

# user registration with checking email already exist
@app.post('/user', status_code=status.HTTP_201_CREATED)
def create(request: User, db: Session = Depends(get_db)):
    user_mail = get_user_by_email(db, email=request.email)
    if user_mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email already registered")

    else:
        new_user = models.User(full_name=request.full_name, email=request.email, phone_number=request.phone_number,
                               password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

# profile picture upload
@app.post("/user/{id}/profile_picture")
def upload_profile_picture(id: int, profile_picture: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    else:
        profile_picture_path = save_profile_picture(profile_picture, id)
        db.Profile.insert_one({"user_id": id, "profile_picture_url": profile_picture_path})
    return user

# getting all user list
@app.get('/user', response_model=List[schemas.ShowUser])
def show_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# get a user with id
@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with an id:{id} not found ')
    return user
