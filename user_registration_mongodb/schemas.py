
from pydantic import BaseModel, EmailStr



class User(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int
    password: str
    profile_picture_url: str

class Profile(BaseModel):
    profile_picture: str

    class Config():
        orm_mode = True

# user details show model
class ShowUser(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int

    class Config():
        orm_mode = True
