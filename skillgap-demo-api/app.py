from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data stays in memory and resets whenever the app restarts.
students = [
    {"id": 1, "name": "Asha Patel", "course": "Computer Science"},
    {"id": 2, "name": "Ravi Kumar", "course": "Information Technology"},
    {"id": 3, "name": "Maya Singh", "course": "Data Science"},
]


@app.get("/students")
def get_students():
    return jsonify(students), 200


@app.get("/students/<int:student_id>")
def get_student(student_id):
    student = next((item for item in students if item["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@app.post("/students")
def add_student():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    name = data.get("name")
    course = data.get("course")
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "'name' is required and must be a non-empty string"}), 400
    if not isinstance(course, str) or not course.strip():
        return jsonify({"error": "'course' is required and must be a non-empty string"}), 400

    next_id = max((student["id"] for student in students), default=0) + 1
    student = {"id": next_id, "name": name.strip(), "course": course.strip()}
    students.append(student)
    return jsonify(student), 201


@app.errorhandler(400)
def bad_request(_error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
