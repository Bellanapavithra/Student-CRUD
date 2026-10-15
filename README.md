# Students Database CRUD Application

**Developed by:** Pavithra

## Project Description
A Python backend application that manages student records using CRUD operations (Create, Read, Update, and Delete). It uses FastAPI to build REST APIs and SQLite to store student information persistently.

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn
- Pydantic
- Swagger UI

## Features
- Add new student records.
- View all students.
- Retrieve individual student details by ID.
- Filter students by name and course.
- Update existing student details.
- Delete student records.
- Store records persistently in an SQLite database.
- Validate request data through Pydantic models.

## Project Structure
```text
studentCRUD/
├── main.py
├── requirements.txt
├── README.md
└── students.db
```

The `students.db` file is created automatically when the application starts. A local `venv/` folder may also be present.

## Installation and Setup

### 1. Clone the repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd studentCRUD
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate it on Windows
```powershell
venv\Scripts\activate
```

### 4. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Run the application
```bash
python -m uvicorn main:app --reload
```

## API Documentation
Open the following URL while the application is running:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List and filter students |
| GET | `/students/{student_id}` | Retrieve a student |
| PUT | `/students/{student_id}` | Update student details |
| DELETE | `/students/{student_id}` | Delete a student |

## Security and Data
Use sample student records for testing. Do not commit real student personal information, passwords, or secrets to GitHub.

## Author
Pavithra
