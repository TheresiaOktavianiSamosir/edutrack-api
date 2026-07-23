from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    judul = Column(String(255), nullable=False)
    deskripsi = Column(Text, nullable=False)
    tipe = Column(String(20), nullable=False)
    deadline = Column(Date, nullable=True)
    benefit = Column(Text, nullable=True)
    dibuat_oleh = Column(Integer, ForeignKey("users.id"))


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    judul = Column(String(255), nullable=False)
    isi_materi = Column(Text, nullable=False)
    urutan = Column(Integer, nullable=False)


class MaterialProgress(Base):
    __tablename__ = "material_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    status_selesai = Column(Boolean, default=False)


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    tanggal_enroll = Column(Date, default=date.today)
    