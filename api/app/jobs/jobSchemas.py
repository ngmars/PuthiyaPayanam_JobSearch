from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyCreate(BaseModel):
    name: str

class CompanyOut(BaseModel):
    name : str

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    company_id: int
    is_remote: Optional[bool] = False
    posted_at: str
    job_url: str

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    company: CompanyOut
    is_remote: Optional[bool] = False
    posted_at: str
    job_url: str
    applications_count: int

    class Config:
        from_attributes = True
    