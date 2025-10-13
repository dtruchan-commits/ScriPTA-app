"""
Test suite for swatch CRUD operations.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from ..main import app


class TestSwatchCRUD:
    """Test swatch CRUD operations"""

    @pytest.mark.asyncio
    async def test_swatch_crud_full_workflow(self):
        """Test complete CRUD workflow for swatch configuration."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test data for a new swatch
            test_swatch = {
                "colorName": "TEST_CRUD_SWATCH",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [100, 50, 25, 10]
            }
            
            # 1. Create a new swatch
            create_response = await ac.post("/create_swatch_config", json=test_swatch)
            assert create_response.status_code == 200
            created_data = create_response.json()
            assert created_data["colorName"] == "TEST_CRUD_SWATCH"
            assert created_data["colorModel"] == "SPOT"
            assert created_data["colorSpace"] == "CMYK"
            assert created_data["colorValues"] == [100, 50, 25, 10]
            
            # 2. Verify the swatch exists by getting it
            get_response = await ac.get("/get_swatch_config?colorName=TEST_CRUD_SWATCH")
            assert get_response.status_code == 200
            get_data = get_response.json()
            assert len(get_data["swatches"]) == 1
            assert get_data["swatches"][0]["colorName"] == "TEST_CRUD_SWATCH"
            
            # 3. Update the swatch
            updated_swatch = {
                "colorName": "TEST_CRUD_SWATCH_UPDATED",
                "colorModel": "PROCESS",
                "colorSpace": "RGB",
                "colorValues": [255, 128, 64]
            }
            update_response = await ac.put("/update_swatch_config/TEST_CRUD_SWATCH", json=updated_swatch)
            assert update_response.status_code == 200
            updated_data = update_response.json()
            assert updated_data["colorName"] == "TEST_CRUD_SWATCH_UPDATED"
            assert updated_data["colorModel"] == "PROCESS"
            assert updated_data["colorSpace"] == "RGB"
            assert updated_data["colorValues"] == [255, 128, 64]
            
            # 4. Verify the update by getting the swatch with new name
            get_updated_response = await ac.get("/get_swatch_config?colorName=TEST_CRUD_SWATCH_UPDATED")
            assert get_updated_response.status_code == 200
            get_updated_data = get_updated_response.json()
            assert len(get_updated_data["swatches"]) == 1
            assert get_updated_data["swatches"][0]["colorName"] == "TEST_CRUD_SWATCH_UPDATED"
            
            # 5. Delete the swatch
            delete_response = await ac.delete("/delete_swatch_config/TEST_CRUD_SWATCH_UPDATED")
            assert delete_response.status_code == 200
            delete_data = delete_response.json()
            assert "deleted successfully" in delete_data["message"]
            
            # 6. Verify the swatch is deleted
            get_deleted_response = await ac.get("/get_swatch_config?colorName=TEST_CRUD_SWATCH_UPDATED")
            assert get_deleted_response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_swatch_success(self):
        """Test successful swatch creation."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            test_swatch = {
                "colorName": "CREATE_TEST_SWATCH",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [0, 100, 50, 0]
            }
            
            # Create swatch
            response = await ac.post("/create_swatch_config", json=test_swatch)
            assert response.status_code == 200
            data = response.json()
            assert data["colorName"] == "CREATE_TEST_SWATCH"
            
            # Cleanup - delete the created swatch
            await ac.delete("/delete_swatch_config/CREATE_TEST_SWATCH")

    @pytest.mark.asyncio
    async def test_create_swatch_duplicate_error(self):
        """Test creating duplicate swatch returns 409 error."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Try to create a swatch with existing color name (DIELINE exists in test data)
            duplicate_swatch = {
                "colorName": "DIELINE",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [0, 100, 100, 0]
            }
            
            response = await ac.post("/create_swatch_config", json=duplicate_swatch)
            assert response.status_code == 409
            data = response.json()
            assert "already exists" in data["detail"]

    @pytest.mark.asyncio
    async def test_update_swatch_not_found(self):
        """Test updating non-existent swatch returns 404."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            test_swatch = {
                "colorName": "NONEXISTENT_UPDATE",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [100, 50, 25, 10]
            }
            
            response = await ac.put("/update_swatch_config/NONEXISTENT_SWATCH", json=test_swatch)
            assert response.status_code == 404
            data = response.json()
            assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_delete_swatch_not_found(self):
        """Test deleting non-existent swatch returns 404."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/delete_swatch_config/NONEXISTENT_DELETE_SWATCH")
            assert response.status_code == 404
            data = response.json()
            assert "not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_update_swatch_success(self):
        """Test successful swatch update with existing swatch."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First create a swatch to update
            original_swatch = {
                "colorName": "UPDATE_TEST_ORIGINAL",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [100, 0, 0, 0]
            }
            
            create_response = await ac.post("/create_swatch_config", json=original_swatch)
            assert create_response.status_code == 200
            
            # Now update it
            updated_swatch = {
                "colorName": "UPDATE_TEST_MODIFIED",
                "colorModel": "PROCESS",
                "colorSpace": "RGB",
                "colorValues": [255, 0, 0]
            }
            
            update_response = await ac.put("/update_swatch_config/UPDATE_TEST_ORIGINAL", json=updated_swatch)
            assert update_response.status_code == 200
            updated_data = update_response.json()
            assert updated_data["colorName"] == "UPDATE_TEST_MODIFIED"
            assert updated_data["colorModel"] == "PROCESS"
            assert updated_data["colorSpace"] == "RGB"
            assert updated_data["colorValues"] == [255, 0, 0]
            
            # Cleanup
            await ac.delete("/delete_swatch_config/UPDATE_TEST_MODIFIED")

    @pytest.mark.asyncio
    async def test_delete_swatch_success(self):
        """Test successful swatch deletion."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First create a swatch to delete
            test_swatch = {
                "colorName": "DELETE_TEST_SWATCH",
                "colorModel": "SPOT",
                "colorSpace": "CMYK",
                "colorValues": [50, 50, 50, 50]
            }
            
            create_response = await ac.post("/create_swatch_config", json=test_swatch)
            assert create_response.status_code == 200
            
            # Delete the swatch
            delete_response = await ac.delete("/delete_swatch_config/DELETE_TEST_SWATCH")
            assert delete_response.status_code == 200
            delete_data = delete_response.json()
            assert "deleted successfully" in delete_data["message"]
            
            # Verify it's actually deleted
            get_response = await ac.get("/get_swatch_config?colorName=DELETE_TEST_SWATCH")
            assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_swatch_crud_with_different_color_models(self):
        """Test CRUD operations with different color models and spaces."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            
            test_cases = [
                {
                    "colorName": "TEST_SPOT_CMYK",
                    "colorModel": "SPOT",
                    "colorSpace": "CMYK",
                    "colorValues": [100, 75, 50, 25]
                },
                {
                    "colorName": "TEST_PROCESS_RGB",
                    "colorModel": "PROCESS",
                    "colorSpace": "RGB",
                    "colorValues": [255, 128, 64]
                },
                {
                    "colorName": "TEST_PROCESS_LAB",
                    "colorModel": "PROCESS",
                    "colorSpace": "LAB",
                    "colorValues": [50, 25, -10]
                }
            ]
            
            created_swatches = []
            
            try:
                # Create all test swatches
                for swatch in test_cases:
                    response = await ac.post("/create_swatch_config", json=swatch)
                    assert response.status_code == 200
                    created_swatches.append(swatch["colorName"])
                    
                    # Verify creation
                    get_response = await ac.get(f"/get_swatch_config?colorName={swatch['colorName']}")
                    assert get_response.status_code == 200
                    
            finally:
                # Cleanup all created swatches
                for color_name in created_swatches:
                    await ac.delete(f"/delete_swatch_config/{color_name}")