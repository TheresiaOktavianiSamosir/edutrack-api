from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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


# ---- Enrollment ----

@app.post("/enrollments", response_model=schemas.EnrollmentResponse)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student sudah terdaftar di course ini")

    new_enrollment = models.Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


@app.get("/students/{student_id}/enrollments", response_model=list[schemas.EnrollmentResponse])
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()


@app.get("/courses/{course_id}/enrollments", response_model=list[schemas.EnrollmentResponse])
def get_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    return db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()


# ---- Tandai Materi Selesai ----

@app.patch("/materials/{material_id}/done", response_model=schemas.MaterialProgressResponse)
def mark_material_done(material_id: int, student_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materi tidak ditemukan")

    progress = db.query(models.MaterialProgress).filter(
        models.MaterialProgress.student_id == student_id,
        models.MaterialProgress.material_id == material_id
    ).first()

    if progress:
        progress.status_selesai = True
    else:
        progress = models.MaterialProgress(
            student_id=student_id,
            material_id=material_id,
            status_selesai=True
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)
    return progress


@app.get("/students/{student_id}/courses/{course_id}/progress", response_model=list[schemas.MaterialProgressResponse])
def get_progress_by_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    materials = db.query(models.Material).filter(models.Material.course_id == course_id).all()
    material_ids = [m.id for m in materials]

    return db.query(models.MaterialProgress).filter(
        models.MaterialProgress.student_id == student_id,
        models.MaterialProgress.material_id.in_(material_ids)
    ).all()

# ---- Dashboard Progres ----

@app.get("/students/{student_id}/dashboard", response_model=list[schemas.DashboardCourseProgress])
def get_dashboard(student_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()

    dashboard_data = []

    for enrollment in enrollments:
        course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
        if not course:
            continue

        materials = db.query(models.Material).filter(models.Material.course_id == course.id).all()
        total_materi = len(materials)
        material_ids = [m.id for m in materials]

        materi_selesai = db.query(models.MaterialProgress).filter(
            models.MaterialProgress.student_id == student_id,
            models.MaterialProgress.material_id.in_(material_ids),
            models.MaterialProgress.status_selesai == True
        ).count()

        persentase = (materi_selesai / total_materi * 100) if total_materi > 0 else 0

        dashboard_data.append(schemas.DashboardCourseProgress(
            course_id=course.id,
            judul_course=course.judul,
            total_materi=total_materi,
            materi_selesai=materi_selesai,
            persentase=round(persentase, 2)
        ))

    return dashboard_data
    