"""Tests for task endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Task, TaskStatus, TaskPriority


class TestTasks:
    """Test cases for task management."""
    
    @pytest.mark.asyncio
    async def test_create_task(self, client: AsyncClient, auth_headers: dict):
        """Test creating a new task."""
        response = await client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Test Task",
                "description": "This is a test task",
                "status": "todo",
                "priority": "high"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["status"] == "todo"
        assert data["priority"] == "high"
        assert "id" in data
        assert "created_at" in data
    
    @pytest.mark.asyncio
    async def test_create_task_without_auth(self, client: AsyncClient):
        """Test creating a task without authentication."""
        response = await client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"}
        )
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_tasks(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test getting all tasks."""
        # Create test tasks
        tasks = [
            Task(title=f"Task {i}", owner_id=test_user.id)
            for i in range(5)
        ]
        for task in tasks:
            db_session.add(task)
        await db_session.commit()
        
        response = await client.get(
            "/api/v1/tasks/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
    
    @pytest.mark.asyncio
    async def test_get_tasks_with_pagination(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test task pagination."""
        # Create 10 tasks
        tasks = [
            Task(title=f"Task {i}", owner_id=test_user.id)
            for i in range(10)
        ]
        for task in tasks:
            db_session.add(task)
        await db_session.commit()
        
        # Get first page
        response = await client.get(
            "/api/v1/tasks/?skip=0&limit=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Get second page
        response = await client.get(
            "/api/v1/tasks/?skip=5&limit=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
    
    @pytest.mark.asyncio
    async def test_get_tasks_by_status(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test filtering tasks by status."""
        # Create tasks with different statuses
        tasks = [
            Task(title="Todo Task", status=TaskStatus.TODO, owner_id=test_user.id),
            Task(title="In Progress Task", status=TaskStatus.IN_PROGRESS, owner_id=test_user.id),
            Task(title="Done Task", status=TaskStatus.DONE, owner_id=test_user.id),
        ]
        for task in tasks:
            db_session.add(task)
        await db_session.commit()
        
        response = await client.get(
            "/api/v1/tasks/?status=todo",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "todo"
    
    @pytest.mark.asyncio
    async def test_get_task_by_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test getting a specific task."""
        task = Task(title="Test Task", owner_id=test_user.id)
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        response = await client.get(
            f"/api/v1/tasks/{task.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == "Test Task"
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_task(self, client: AsyncClient, auth_headers: dict):
        """Test getting a nonexistent task."""
        response = await client.get(
            "/api/v1/tasks/99999",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_task(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test updating a task."""
        task = Task(title="Old Title", owner_id=test_user.id)
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        response = await client.put(
            f"/api/v1/tasks/{task.id}",
            headers=auth_headers,
            json={
                "title": "New Title",
                "status": "in_progress"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["status"] == "in_progress"
    
    @pytest.mark.asyncio
    async def test_update_task_to_done_sets_completed_at(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test that completing a task sets completed_at."""
        task = Task(title="Test Task", status=TaskStatus.TODO, owner_id=test_user.id)
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        response = await client.put(
            f"/api/v1/tasks/{task.id}",
            headers=auth_headers,
            json={"status": "done"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "done"
        assert data["completed_at"] is not None
    
    @pytest.mark.asyncio
    async def test_delete_task(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test deleting a task."""
        task = Task(title="Test Task", owner_id=test_user.id)
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        response = await client.delete(
            f"/api/v1/tasks/{task.id}",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify task is deleted
        response = await client.get(
            f"/api/v1/tasks/{task.id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_task_stats(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        test_user: User
    ):
        """Test getting task statistics."""
        # Create tasks with different statuses
        tasks = [
            Task(title="Todo 1", status=TaskStatus.TODO, owner_id=test_user.id),
            Task(title="Todo 2", status=TaskStatus.TODO, owner_id=test_user.id),
            Task(title="In Progress", status=TaskStatus.IN_PROGRESS, owner_id=test_user.id),
            Task(title="Done", status=TaskStatus.DONE, owner_id=test_user.id),
        ]
        for task in tasks:
            db_session.add(task)
        await db_session.commit()
        
        response = await client.get(
            "/api/v1/tasks/stats/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 4
        assert data["by_status"]["todo"] == 2
        assert data["by_status"]["in_progress"] == 1
        assert data["by_status"]["done"] == 1
