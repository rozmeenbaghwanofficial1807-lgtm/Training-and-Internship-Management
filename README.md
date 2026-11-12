# Training & Internship Management System

A beginner-friendly Flask + MySQL web application with three roles: Admin, Student and Company.

## 1. Requirements
- Python 3.10 or newer
- MySQL Server running locally
- VS Code (recommended)

## 2. Create the MySQL database
Open MySQL Workbench or the MySQL command line and run:
```sql
CREATE DATABASE training_internship_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. Configure environment
In this project folder, copy `.env.example` to `.env`.
Update `DATABASE_URL` with your MySQL username and password. Example:
`mysql+pymysql://root:MyPassword@localhost:3306/training_internship_db`
Change `SECRET_KEY` and `ADMIN_PASSWORD` before using the application.

## 4. Install and run (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
If PowerShell blocks activation, run this once in the same terminal:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
Then activate the environment again.

Open http://127.0.0.1:5000

## 5. First login
The application creates the first admin account automatically using `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `.env`.
Default example credentials (only if you did not change `.env`):
- Email: `admin@example.com`
- Password: `ChangeThisAdminPassword123!`

Change the default password before real use. Do not publish `.env` or upload it to GitHub.

## 6. Basic workflow
1. Register a Student account.
2. Register a Company account.
3. Sign in as Admin and approve the company.
4. Sign in as the approved Company and post an internship.
5. Admin approves the internship.
6. Student completes their profile and uploads a resume.
7. Student applies; Company reviews the application and updates its status.

## 7. Notes
- Resume uploads accept PDF, DOC and DOCX up to 5 MB.
- SQLAlchemy creates the tables automatically on first run.
- `db.create_all()` is suitable for this starter project. For future schema changes, use Flask-Migrate.
- This is a college-project starter, not a production deployment. Before public deployment, add CSRF protection, email verification, password reset, stronger upload scanning, rate limiting, audit logs, HTTPS and production server configuration.
