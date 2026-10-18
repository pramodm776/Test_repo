# SkillGap Demo

A small full-stack skills tracker demonstrating a Python/Flask API, SQLite queries, automated API tests, a React UI with HTML/CSS, and a Java API client. The nine skills from the brief are seeded as required skills.

## Start the API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Flask creates `skills.db` on first start and listens at `http://127.0.0.1:5000`.

## Start the React page

In a second PowerShell window in this folder:

```powershell
python -m http.server 8000
```

Open `http://127.0.0.1:8000`. The browser page uses React from esm.sh, so internet access is needed to load the React modules and Google Fonts.

## API

- `GET /skills` lists skills.
- `POST /skills` adds a skill. JSON: `{"name":"Docker","proficiency":2}`; proficiency is 0–5.
- `PATCH /skills/<id>` changes proficiency. JSON: `{"proficiency":4}`.

The UI shows required skills, lets you set proficiency, and lets you add skills. The Java sample fetches the list from the API.

## Automated tests

```powershell
pytest
```

Tests use a temporary SQLite database and cover seeded skills, adding, duplicate handling, proficiency updates, and validation.

## Java client

Requires JDK 11 or newer:

```powershell
javac java\SkillsClient.java
java -cp java SkillsClient
```

## Git and GitHub

Initialize version control with `git init`, then stage and commit with `git add .` and `git commit -m "Build skills tracker demo"`. Create an empty GitHub repository and connect it with `git remote add origin <repository-url>`, then push the branch with `git push -u origin HEAD`.
