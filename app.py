"""SQLite-backed skills catalog API."""
import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = Path(os.environ.get("SKILLS_DATABASE", Path(__file__).with_name("skills.db")))
SEED_SKILLS = ["API development", "SQL and database queries", "Automated testing", "Python",
               "JavaScript", "React", "HTML and CSS", "Java", "Git and GitHub"]


@app.after_request
def enable_local_ui(response):
    # Allow the development server (python -m http.server 8000) to call this API.
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
    return response


def connect_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def initialize_db():
    with connect_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            required INTEGER NOT NULL DEFAULT 1 CHECK (required IN (0, 1)),
            proficiency INTEGER NOT NULL DEFAULT 0 CHECK (proficiency BETWEEN 0 AND 5)
        )""")
        db.executemany("INSERT OR IGNORE INTO skills (name) VALUES (?)", [(name,) for name in SEED_SKILLS])


def skill_json(row):
    return {"id": row["id"], "name": row["name"], "required": bool(row["required"]),
            "proficiency": row["proficiency"]}


@app.get("/")
def home():
    return jsonify({"message": "Skills Gap Demo API", "skills": "/skills"})


@app.get("/skills")
def get_skills():
    with connect_db() as db:
        rows = db.execute("SELECT * FROM skills ORDER BY id").fetchall()
    return jsonify([skill_json(row) for row in rows])


@app.post("/skills")
def add_skill():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    name, proficiency = data.get("name"), data.get("proficiency", 0)
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "'name' is required and must be a non-empty string"}), 400
    if type(proficiency) is not int or not 0 <= proficiency <= 5:
        return jsonify({"error": "'proficiency' must be an integer from 0 to 5"}), 400
    try:
        with connect_db() as db:
            cursor = db.execute("INSERT INTO skills (name, proficiency) VALUES (?, ?)",
                                (name.strip(), proficiency))
            row = db.execute("SELECT * FROM skills WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A skill with that name already exists"}), 409
    return jsonify(skill_json(row)), 201


@app.patch("/skills/<int:skill_id>")
def update_skill(skill_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    proficiency = data.get("proficiency")
    if type(proficiency) is not int or not 0 <= proficiency <= 5:
        return jsonify({"error": "'proficiency' must be an integer from 0 to 5"}), 400
    with connect_db() as db:
        cursor = db.execute("UPDATE skills SET proficiency = ? WHERE id = ?", (proficiency, skill_id))
        row = db.execute("SELECT * FROM skills WHERE id = ?", (skill_id,)).fetchone()
    if cursor.rowcount == 0:
        return jsonify({"error": "Skill not found"}), 404
    return jsonify(skill_json(row))


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
