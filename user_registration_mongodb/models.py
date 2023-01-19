from sqlalchemy import Column, Integer, String
import database

Base = database.Base


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(Integer)
    password = Column(String)


class Profile(Base):
    __tablename__ = 'Profile'

    user_id = Column(Integer, primary_key=True, index=True)
    profile_picture_url = Column(String)
