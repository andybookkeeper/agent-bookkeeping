"""
Basic tests for the bookkeeping API
Run with: pytest
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthCheck:
    """Health check endpoint tests"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "message" in data


class TestAccountsEndpoints:
    """Account endpoints tests"""
    
    def test_list_accounts_empty(self):
        """Test listing accounts when empty"""
        response = client.get("/api/accounts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_nonexistent_account(self):
        """Test getting non-existent account"""
        response = client.get("/api/accounts/nonexistent")
        assert response.status_code == 404


class TestDocumentation:
    """Documentation endpoints tests"""
    
    def test_swagger_docs(self):
        """Test Swagger documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
