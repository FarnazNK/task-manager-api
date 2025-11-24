"""Integration tests for end-to-end workflows."""
import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestUserTaskWorkflow:
    """Test complete user and task workflow."""
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, client: AsyncClient):
        """Test complete user registration, login, and task management workflow."""
        
        # 1. Register a new user
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "workflow@example.com",
                "username": "workflowuser",
                "full_name": "Workflow User",
                "password": "WorkflowPass123!"
            }
        )
        assert register_response.status_code == 201
        user_data = register_response.json()
        assert user_data["username"] == "workflowuser"
        
        # 2. Login with the new user
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "workflowuser",
                "password": "WorkflowPass123!"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get user profile
        profile_response = await client.get(
            "/api/v1/users/me",
            headers=headers
        )
        assert profile_response.status_code == 200
        assert profile_response.json()["email"] == "workflow@example.com"
        
        # 4. Create a task
        task_response = await client.post(
            "/api/v1/tasks/",
            headers=headers,
            json={
                "title": "Integration Test Task",
                "description": "This is a test task",
                "priority": "high"
            }
        )
        assert task_response.status_code == 201
        task_data = task_response.json()
        task_id = task_data["id"]
        
        # 5. Get all tasks
        tasks_response = await client.get(
            "/api/v1/tasks/",
            headers=headers
        )
        assert tasks_response.status_code == 200
        assert len(tasks_response.json()) == 1
        
        # 6. Update task status
        update_response = await client.put(
            f"/api/v1/tasks/{task_id}",
            headers=headers,
            json={"status": "done"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "done"
        assert update_response.json()["completed_at"] is not None
        
        # 7. Get task statistics
        stats_response = await client.get(
            "/api/v1/tasks/stats/summary",
            headers=headers
        )
        assert stats_response.status_code == 200
        stats = stats_response.json()
        assert stats["total_tasks"] == 1
        assert stats["by_status"]["done"] == 1
        
        # 8. Delete the task
        delete_response = await client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=headers
        )
        assert delete_response.status_code == 204
        
        # 9. Verify task is deleted
        tasks_after_delete = await client.get(
            "/api/v1/tasks/",
            headers=headers
        )
        assert len(tasks_after_delete.json()) == 0
