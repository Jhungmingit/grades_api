from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Course, Grade
from schemas import CourseCreate, CourseOut, CourseUpdate, GradeCreate, GradeOut, GradeUpdate, StudentAverage, StudentCreate, StudentUpdate, StudentOut, CourseAverage
from sqlalchemy import func

app = FastAPI() 

#CREATE STUDENT
@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
     
    student = Student(
        full_name=payload.full_name,
        email=payload.email,
        birth_date=payload.birth_date,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

#GET LIST OF STUDENTS
@app.get("/students", response_model=list[StudentOut], status_code=200)
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if name:
        query = query.filter(Student.full_name.ilike(f"%{name}%"))

    return (
        query
        .order_by(Student.student_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

#GET 1 STUDENT   
@app.get("/students/{student_id}", response_model=StudentOut, status_code=200)  
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

#UPDATE STUDENT 
@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)                    
    changes = payload.model_dump(exclude_unset=True)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if "email" in changes and changes["email"] != student.email:    
        taken = db.query(Student).filter(Student.email == changes["email"],
            Student.student_id != student_id
        ).first()
        if taken:
            raise HTTPException(status_code=409, detail="Email already taken")

    for field, value in changes.items():
        setattr(student, field, value)                           

    db.commit()
    db.refresh(student)
    return student

#DELETE STUDENT 
@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.query(Grade).filter(Grade.student_id == student_id).delete()
    db.delete(student)
    db.commit()
    

#Create Course
@app.post("/courses", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):

    course = Course(
        course_name=payload.course_name,
        instructor_name=payload.instructor_name,
        credits=payload.credits
    )

    db.add(course)
    db.commit()
    db.refresh(course)
    return course

#GET 1 COURSE
@app.get("/courses/{course_id}", response_model=CourseOut, status_code=200)  
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# GET LIST OF COURSES
@app.get("/courses", response_model=list[CourseOut])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(Course)
        .order_by(Course.course_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

#UPDATE COURSE
@app.patch("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    changes = payload.model_dump(exclude_unset=True)
    if course is None:
            raise HTTPException(status_code=404, detail="Course not found")

    for field, value in changes.items():
            setattr(course, field, value)                            
    
    db.commit()
    db.refresh(course)
    return course

# DELETE COURSE
@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    has_grades = db.query(Grade).filter(Grade.course_id == course_id).first()
    if has_grades:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a course that still has grades",
        )

    db.delete(course)
    db.commit()
        
# CREATE GRADE
@app.post("/grades", response_model=GradeOut, status_code=201)
def create_grade(payload: GradeCreate, db: Session = Depends(get_db)):
    student = db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=400, detail="Student not found")

    course = db.get(Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")

    existing = (
        db.query(Grade)
        .filter(
            Grade.student_id == payload.student_id,
            Grade.course_id == payload.course_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Student already has a grade in this course"
        )

    new_grade = Grade(
        student_id=payload.student_id,
        course_id=payload.course_id,
        grade=payload.grade, 
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

# GET 1 GRADE
@app.get("/students/{student_id}/grades", response_model=list[GradeOut])  
def get_student_grades(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return (
        db.query(Grade)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.grade_id)
        .all()
    )

# UPDATE GRADE
@app.patch("/grades/{grade_id}", response_model=GradeOut)
def update_grade(grade_id: int, payload: GradeUpdate, db: Session = Depends(get_db)):
    grade = db.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(grade, field, value)

    db.commit()
    db.refresh(grade)
    return grade
 
 #DELETE GRADE 
@app.delete("/grades/{grade_id}", status_code=204)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.get(Grade, grade_id)
    if grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")

    db.delete(grade)
    db.commit()

# REPORTS/ GRADE AVERAGE
@app.get("/reports/student-averages", response_model=list[StudentAverage])
def student_averages(db: Session = Depends(get_db)): 
    return (
      db.query(
        Student.student_id,
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label("average_grade"),
        func.count(Grade.grade_id).label("courses_taken"),
    )
      .join(Grade, Grade.student_id == Student.student_id)
      .group_by(Student.student_id, Student.full_name)
      .order_by(Student.student_id)
      .all()
)

# REPORT/ COURSE AVERAGE
@app.get("/reports/course-averages", response_model=list[CourseAverage])
def course_averages(db: Session = Depends(get_db)):
    return (
        db.query(
            Course.course_id,
            Course.course_name, 
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            func.count(Grade.grade_id).label("students_graded")
        )
        .join(Grade, Grade.course_id == Course.course_id)
        .group_by(Course.course_id, Course.course_name)
        .order_by(Course.course_id)
        .all()
    )
