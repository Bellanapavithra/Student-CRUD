
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Students Database CRUD Application")

DATABASE = "students.db"


# Create the database and table
def create_table():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            course TEXT,
            address TEXT,
            enrollment_date TEXT
        )
    """)

    conn.commit()
    conn.close()


create_table()


# Student details required when creating a record
class StudentCreate(BaseModel):
    name: str
    date_of_birth: str
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


# Fields that can be changed when updating a record
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


# CREATE: Add a student
@app.post("/students")
def create_student(student: StudentCreate):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute("""
        INSERT INTO students
        (name, date_of_birth, email, phone, course, address, enrollment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student.name,
        student.date_of_birth,
        student.email,
        student.phone,
        student.course,
        student.address,
        student.enrollment_date
    ))

    student_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Student created successfully",
        "student_id": student_id
    }


# READ: Get all students or filter by name/course
@app.get("/students")
def get_students(
    name: Optional[str] = None,
    course: Optional[str] = None
):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = "SELECT * FROM students WHERE 1=1"
    values = []

    if name:
        query += " AND name LIKE ?"
        values.append("%" + name + "%")

    if course:
        query += " AND course LIKE ?"
        values.append("%" + course + "%")

    rows = conn.execute(query, values).fetchall()
    conn.close()

    return [dict(row) for row in rows]


# READ: Get one student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return dict(row)


# UPDATE: Change student details
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    updates = student.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    conn = sqlite3.connect(DATABASE)

    existing = conn.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    columns = ", ".join(key + " = ?" for key in updates)
    values = list(updates.values()) + [student_id]

    conn.execute(
        f"UPDATE students SET {columns} WHERE student_id = ?",
        values
    )

    conn.commit()
    conn.close()

    return {"message": "Student updated successfully"}


# DELETE: Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"message": "Student deleted successfully"}
