from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field

# STUDENT
class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    birth_date: date | None = None

class StudentUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    birth_date: date | None = None

class StudentOut(BaseModel):                         # What our api sends out to the client
    model_config = ConfigDict(from_attributes=True)  # our route will return a SQLAlchemy Student object, not a dict. This setting tells Pydantic to read the values from the object’s attributes (student.full_name) instead of expecting dictionary keys.
    full_name: str
    email: EmailStr
    birth_date: date | None = None
    student_id: int
    enrollment_date: date


# COURSE 
class CourseCreate(BaseModel):
    course_name: str
    instructor_name: str
    credits: int = Field(gt=0)

class CourseUpdate(BaseModel):
    course_name: str | None = None
    instructor_name: str | None = None
    credits: int | None = Field(default=None, gt=0)

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    course_id: int
    course_name: str
    instructor_name: str
    credits: int 


# GRADE
class GradeCreate(BaseModel):
    student_id: int
    course_id: int 
    grade: float = Field(ge=0, le=100)

class GradeUpdate(BaseModel):                       # Removed both columns because moving grades to a different student isnt updating
    grade: float = Field(ge=0, le=100)

class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    grade_id: int
    student_id: int
    course_id: int 
    grade: float

class StudentAverage(BaseModel):
    student_id: int
    full_name: str
    average_grade: float
    courses_taken: int
    model_config = ConfigDict(from_attributes=True)

class CourseAverage(BaseModel):
    course_id: int
    course_name: str
    average_grade: float
    students_graded: int
    model_config = ConfigDict(from_attributes=True)
