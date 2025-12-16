from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email : EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class userDetailsCreate(BaseModel):
    website_link: str
    is_cv: Optional[bool] = False
    is_linkedIn: Optional[bool] = False
    is_github : Optional[bool] = False
    other_site: Optional[str] = None

class userDetailsOut(BaseModel):
    id: int
    website_link: str
    is_cv: Optional[bool] = False
    is_linkedIn: Optional[bool] = False
    is_github : Optional[bool] = False
    other_site: Optional[str] = None

    class Config:
        from_attributes = True
        
class userDetailsUpdate(BaseModel):
    website_link: str
    is_cv: Optional[bool] = False
    is_linkedIn: Optional[bool] = False
    is_github : Optional[bool] = False
    other_site: Optional[str] = None