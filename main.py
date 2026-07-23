from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import models
import schemas
import auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "EduTrack API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---- CRUD Course ----

@app.post("/courses", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get("/courses", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    return course


@app.put("/courses/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    for key, value in updated_course.dict().items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course tidak ditemukan")
    db.delete(course)
    db.commit()
    return {"message": "Course berhasil dihapus"}

# ---- CRUD Materi ----

@app.post("/materials", response_model=schemas.MaterialResponse)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    new_material = models.Material(**material.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


@app.get("/materials", response_model=list[schemas.MaterialResponse])
def get_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()


@app.get("/courses/{course_id}/materials", response_model=list[schemas.MaterialResponse])
def get_materials_by_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(models.Material).filter(models.Material.course_id == course_id).order_by(models.Material.urutan).all()


@app.put("/materials/{material_id}", response_model=schemas.MaterialResponse)
def update_material(material_id: int, updated_material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materi tidak ditemukan")
    for key, value in updated_material.dict().items():
        setattr(material, key, value)
    db.commit()
    db.refresh(material)
    return material


@app.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materi tidak ditemukan")
    db.delete(material)
    db.commit()
    return {"message": "Materi berhasil dihapus"}

# ---- Autentikasi ----

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah digunakan")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    access_token = auth.create_access_token(data={"user_id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
