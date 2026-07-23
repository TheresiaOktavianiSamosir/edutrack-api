from pydantic import BaseModel
from typing import Optional
from datetime import date

class CourseBase(BaseModel):
    judul: str
    deskripsi: str
    tipe: str
    deadline: Optional[date] = None
    benefit: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    dibuat_oleh: Optional[int] = None

    class Config:
        from_attributes = True

class MaterialBase(BaseModel):
    course_id: int
    judul: str
    isi_materi: str
    urutan: int

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    