"""Tests for user endpoints."""
import pytest
from httpx import AsyncClient

from app.models import User


class TestUsers:
    """Test cases for user management."""
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient, auth_headers: dict, test_user: User):
        """Test getting current user profile."""
        response = await client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert "hashed_password" not in data
    
    @pytest.mark.asyncio
    async def test_get_current_user_without_auth(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_update_current_user(self, client: AsyncClient, auth_headers: dict):
        """Test updating current user profile."""
        response = await client.put(
            "/api/v1/users/me",
            headers=auth_headers,
            json={
                "full_name": "Updated Name",
                "email": "updated@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["email"] == "updated@example.com"
    
    @pytest.mark.asyncio
    async def test_update_password(self, client: AsyncClient, auth_headers: dict):
        """Test updating user password."""
        response = await client.put(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"password": "NewPassword123!"}
        )
        assert response.status_code == 200
        
        # Try logging in with new password
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "NewPassword123!"
            }
        )
        assert login_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_delete_current_user(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test deleting current user account."""
        response = await client.delete(
            "/api/v1/users/me",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify user cannot access their profile anymore
        profile_response = await client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        assert profile_response.status_code == 401
