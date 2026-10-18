# SkillGap Demo API

A small Student Directory REST API built with Flask. It demonstrates basic REST endpoints, input validation, and JSON HTTP error responses. Student records are stored in a Python list in memory, so additions are lost when the application stops.

## Requirements

- Python 3.9 or newer
- pip

## Install and run

From this directory, create and activate a virtual environment, then install Flask:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The development server runs at `http://127.0.0.1:5000`.

## Endpoints

- `GET /students` — return all sample students.
- `GET /students/<id>` — return one student, or a JSON 404 error if the ID does not exist.
- `POST /students` — add a student. Send a JSON object with non-empty string fields `name` and `course`. A successful response has status `201`.

Example PowerShell requests (while the server is running):

```powershell
Invoke-RestMethod http://127.0.0.1:5000/students
Invoke-RestMethod http://127.0.0.1:5000/students/1
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/students -ContentType 'application/json' -Body '{"name":"Jordan Lee","course":"AI Engineering"}'
```

To see validation errors, try a missing student ID or send invalid JSON data:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/students/999
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/students -ContentType 'application/json' -Body '{"name":"","course":"AI Engineering"}'
```

PowerShell may display non-2xx response details as an exception; the API response body contains a JSON `error` message.

## Current scope

This initial demo uses in-memory data. It does not include a database, automated tests, Docker, CI/CD, or deployment configuration.
