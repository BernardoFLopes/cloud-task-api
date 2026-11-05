import pytest
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_health(client):
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json["status"] == "ok"


def test_create_and_list(client):
    result = client.post("/tasks", json={"title": "Estudar GitHub Actions"})
    assert result.status_code == 201
    assert result.json["id"] == 1
    listed = client.get("/tasks")
    assert listed.status_code == 200
    assert len(listed.json) == 1
    assert listed.json[0]["title"] == "Estudar GitHub Actions"


def test_invalid_title(client):
    assert client.post("/tasks", json={"title": "  "}).status_code == 400


def test_mark_done(client):
    item = client.post("/tasks", json={"title": "Deploy"}).json
    result = client.patch(f'/tasks/{item["id"]}', json={"done": True})
    assert result.status_code == 200
    assert client.get("/tasks").json[0]["done"] is True


def test_not_found(client):
    assert client.patch("/tasks/999", json={"done": True}).status_code == 404


def test_delete_task_success(client):
    item = client.post("/tasks", json={"title": "Tarefa para excluir"}).json
    result = client.delete(f'/tasks/{item["id"]}')
    assert result.status_code == 204
    assert client.get("/tasks").json == []


def test_delete_task_not_found(client):
    result = client.delete("/tasks/999")
    assert result.status_code == 404


def test_filter_tasks_by_done(client):
    t1 = client.post("/tasks", json={"title": "Pendente"}).json
    t2 = client.post("/tasks", json={"title": "Concluida"}).json
    client.patch(f'/tasks/{t2["id"]}', json={"done": True})

    done_tasks = client.get("/tasks?done=true").json
    assert len(done_tasks) == 1
    assert done_tasks[0]["id"] == t2["id"]

    pending_tasks = client.get("/tasks?done=false").json
    assert len(pending_tasks) == 1
    assert pending_tasks[0]["id"] == t1["id"]

