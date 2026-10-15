def test_health(client):
    """M1/M2 Criterion: /health responds with UP status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_ready(client):
    """M1/M2 Criterion: /ready verifies database access."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}


def test_root(client):
    """M1/M2 Criterion: / returns service information and docs URL."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["docs"] == "/docs"


def test_create_task(client):
    """M1/M2 Criterion: POST /api/tasks creates a new task."""
    payload = {
        "title": "Configure EKS Cluster",
        "description": "Deploy AWS EKS managed node group using Terraform",
        "priority": "HIGH",
        "status": "TODO",
        "assignee": "DevOps Engineer"
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["priority"] == "HIGH"
    assert data["status"] == "TODO"
    assert "id" in data
    assert "created_at" in data


def test_create_task_validation_error(client):
    """M1/M2 Criterion: POST /api/tasks validates required fields."""
    # Empty title should fail validation (min_length=1)
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks(client):
    """M1/M2 Criterion: GET /api/tasks lists tasks in database."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_task_by_id(client):
    """M1/M2 Criterion: GET /api/tasks/{id} retrieves an existing task."""
    # Create a task to fetch
    create_res = client.post("/api/tasks", json={"title": "Write Unit Tests", "priority": "MEDIUM"})
    task_id = create_res.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Write Unit Tests"


def test_get_task_not_found(client):
    """M1/M2 Criterion: GET /api/tasks/{id} returns 404 for non-existent task."""
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    """M1/M2 Criterion: PUT /api/tasks/{id} updates task fields."""
    create_res = client.post("/api/tasks", json={"title": "Setup Ingress", "status": "TODO"})
    task_id = create_res.json()["id"]

    update_payload = {"status": "IN_PROGRESS", "priority": "HIGH"}
    response = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
    assert response.json()["priority"] == "HIGH"


def test_task_stats(client):
    """M1/M2 Criterion: GET /api/tasks/stats returns task counts by status."""
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "todo" in data
    assert "inProgress" in data
    assert "done" in data
    assert data["total"] >= 1


def test_delete_task(client):
    """M1/M2 Criterion: DELETE /api/tasks/{id} removes a task."""
    create_res = client.post("/api/tasks", json={"title": "Temporary Task"})
    task_id = create_res.json()["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verification: should now return 404
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404
