import pytest

@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post("/tasks", json={
        "task_name": "Test Task",
        "task_status": "Pending"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["task_name"] == "Test Task"
    assert data["task_status"] == "Pending"
    assert "task_id" in data
