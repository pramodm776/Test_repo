import pytest
import app as skills_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(skills_app, "DATABASE", tmp_path / "test.db")
    skills_app.initialize_db()
    return skills_app.app.test_client()


def test_seed_skills_are_required(client):
    response = client.get("/skills")
    assert response.status_code == 200
    assert len(response.json) == 9
    assert all(item["required"] for item in response.json)


def test_add_skill_and_reject_duplicate(client):
    response = client.post("/skills", json={"name": "Docker", "proficiency": 2})
    assert response.status_code == 201
    assert response.json["name"] == "Docker"
    assert client.post("/skills", json={"name": "Docker"}).status_code == 409


def test_update_proficiency(client):
    response = client.patch("/skills/1", json={"proficiency": 4})
    assert response.status_code == 200
    assert response.json["proficiency"] == 4


def test_invalid_proficiency_is_rejected(client):
    assert client.post("/skills", json={"name": "Docker", "proficiency": 8}).status_code == 400
