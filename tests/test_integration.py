import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from main import app


class TestAsyncEndpoints:
    """Tests for async endpoint functionality"""
    
    @pytest.mark.asyncio
    async def test_async_root_endpoint(self):
        """Test root endpoint using async client."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "ScriPTA", "version": "1.0.0"}
    
    @pytest.mark.asyncio
    async def test_async_get_swatch_config_all(self):
        """Test get_swatch_config endpoint without filter using async client."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/get_swatch_config")
        
        assert response.status_code == 200
        data = response.json()
        assert "swatches" in data
        assert len(data["swatches"]) > 0
    
    @pytest.mark.asyncio
    async def test_async_get_swatch_config_with_filter(self):
        """Test get_swatch_config endpoint with filter using async client."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/get_swatch_config?colorName=DIELINE")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["swatches"]) == 1
        assert data["swatches"][0]["colorName"] == "DIELINE"
    
    @pytest.mark.asyncio
    async def test_async_get_swatch_config_not_found(self):
        """Test get_swatch_config endpoint with invalid color name using async client."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/get_swatch_config?colorName=INVALID")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestIntegrationScenarios:
    """Integration tests simulating real-world usage scenarios"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow_scenario(self):
        """Test a complete workflow: check API info, then query specific swatch."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First, check if API is available
            root_response = await ac.get("/")
            assert root_response.status_code == 200
            
            # Then, get all swatches to see what's available
            all_swatches_response = await ac.get("/get_swatch_config")
            assert all_swatches_response.status_code == 200
            all_swatches = all_swatches_response.json()["swatches"]
            
            # Pick the first swatch and query it specifically
            if all_swatches:
                first_color_name = all_swatches[0]["colorName"]
                specific_response = await ac.get(f"/get_swatch_config?colorName={first_color_name}")
                assert specific_response.status_code == 200
                
                specific_swatch = specific_response.json()["swatches"][0]
                assert specific_swatch["colorName"] == first_color_name
    
    def test_concurrent_requests_sync(self, client):
        """Test that multiple concurrent synchronous requests work correctly."""
        import concurrent.futures
        
        def make_request(color_name):
            return client.get(f"/get_swatch_config?colorName={color_name}")
        
        # Test concurrent requests for different color names
        color_names = ["DIELINE", "PA123", "PA321"]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, name) for name in color_names]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for result in results:
            assert result.status_code == 200
            data = result.json()
            assert len(data["swatches"]) == 1


class TestPerformanceAndLoad:
    """Basic performance tests"""
    
    def test_response_time_acceptable(self, client):
        """Test that response times are reasonable."""
        import time
        
        start_time = time.time()
        response = client.get("/get_swatch_config")
        end_time = time.time()
        
        assert response.status_code == 200
        # Response should be faster than 1 second (generous for unit test)
        assert (end_time - start_time) < 1.0
    
    def test_multiple_rapid_requests(self, client):
        """Test handling of multiple rapid requests."""
        # Make 10 rapid requests
        responses = []
        for _ in range(10):
            response = client.get("/get_swatch_config")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "swatches" in data
