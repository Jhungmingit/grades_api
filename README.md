# Grades API

A FastAPI backend for managing students, courses, and grades, stored in PostgreSQL.

## 1. Create the database

Start the container, create the `school` database, and load the schema:

```bash
docker start pg
docker exec pg psql -U postgres -c "CREATE DATABASE school"
docker exec -i pg psql -U postgres -d school < student_grades.sql
```

## 2. Set up .env

Create a file named `.env` in the project folder with one line

```

## 3. Install and run

```bash
python -m venv .venv  
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

Then open http://127.0.0.1:8000/docs

To run the tests: `pytest -v`

## 4. Student vs. course delete

For a real school, I would block the course delete if any grades are left in it. If someone deleted a course by accident and every student's grades in it were deleted too, it would take much more time and effort to restore than deleting a single student and their grades.


