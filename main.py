from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StudentSchema(BaseModel):
    name: str
    age: int
    course: str

# CREATE
@app.post("/students")
def add_student(student: StudentSchema, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# READ ALL
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# READ ONE
@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Not found")
    return student

# UPDATE
@app.put("/students/{id}")
def update_student(id: int, student: StudentSchema, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Not found")

    db_student.name = student.name
    db_student.age = student.age
    db_student.course = student.course

    db.commit()
    return {"message": "Updated"}

# DELETE
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Deleted"}

# BONUS: SEARCH
@app.get("/search")
def search(name: str, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.name.contains(name)).all()

def add_numbers(a, b):
    return a + b