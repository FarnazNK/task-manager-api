"""Tests for main application endpoints."""
import pytest
from httpx import AsyncClient


class TestMainApp:
    """Test cases for main application."""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint returns health status."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
        assert "version" in data
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "api_version" in data
    
    @pytest.mark.asyncio
    async def test_docs_endpoint(self, client: AsyncClient):
        """Test API documentation is accessible."""
        response = await client.get("/docs")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_redoc_endpoint(self, client: AsyncClient):
        """Test ReDoc documentation is accessible."""
        response = await client.get("/redoc")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_security_headers(self, client: AsyncClient):
        """Test security headers are present."""
        response = await client.get("/")
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"
        assert "x-xss-protection" in response.headers
