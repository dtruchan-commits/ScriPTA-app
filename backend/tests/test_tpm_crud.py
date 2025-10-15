"""
Test suite for TPM CRUD operations.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from ..main import app


class TestTpmCRUD:
    """Test TPM CRUD operations"""

    @pytest.mark.asyncio
    async def test_get_all_tpm_configs(self):
        """Test getting all TPM configurations."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/get_tpm_config")
            
            assert response.status_code == 200
            data = response.json()
            assert "tpms" in data
            assert isinstance(data["tpms"], list)
            # Should have at least some TPM records from the database
            assert len(data["tpms"]) > 0
            
            # Check structure of first TPM record
            first_tpm = data["tpms"][0]
            assert "id" in first_tpm
            assert "TPM" in first_tpm
            assert isinstance(first_tpm["id"], int)
            assert isinstance(first_tpm["TPM"], str)

    @pytest.mark.asyncio
    async def test_get_tpm_config_by_name(self):
        """Test getting TPM configuration by name."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First get all TPMs to find a valid name
            all_response = await ac.get("/get_tpm_config")
            all_data = all_response.json()
            
            if len(all_data["tpms"]) > 0:
                existing_tpm_name = all_data["tpms"][0]["TPM"]
                
                # Test filtering by name
                response = await ac.get(f"/get_tpm_config?tpmName={existing_tpm_name}")
                assert response.status_code == 200
                
                data = response.json()
                assert "tpms" in data
                assert len(data["tpms"]) >= 1
                
                # All returned TPMs should have the specified name
                for tpm in data["tpms"]:
                    assert tpm["TPM"] == existing_tpm_name

    @pytest.mark.asyncio
    async def test_get_tpm_config_nonexistent_name(self):
        """Test getting TPM configuration with non-existent name."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/get_tpm_config?tpmName=NONEXISTENT_TPM_NAME")
            assert response.status_code == 404
            error_data = response.json()
            assert "detail" in error_data
            assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_tpm_by_id_existing(self):
        """Test getting a specific TPM by ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First get all TPMs to find a valid ID
            all_response = await ac.get("/get_tpm_config")
            all_data = all_response.json()
            
            if len(all_data["tpms"]) > 0:
                existing_id = all_data["tpms"][0]["id"]
                
                response = await ac.get(f"/get_tpm_by_id/{existing_id}")
                assert response.status_code == 200
                
                data = response.json()
                assert data["id"] == existing_id
                assert "TPM" in data
                assert isinstance(data["TPM"], str)

    @pytest.mark.asyncio
    async def test_get_tpm_by_id_nonexistent(self):
        """Test getting TPM by non-existent ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Use a very high ID that shouldn't exist
            response = await ac.get("/get_tpm_by_id/99999")
            assert response.status_code == 404
            error_data = response.json()
            assert "detail" in error_data
            assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_tpm_success(self):
        """Test creating a new TPM configuration."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            test_tpm = {
                "TPM": "TEST_CREATE_TPM",
                "description": "Test TPM for creation",
                "A": 150,
                "B": 250,
                "H": 75,
                "variant": "v1.0",
                "version": 1,
                "packType": "box",
                "comment": "Test comment"
            }
            
            response = await ac.post("/create_tpm", json=test_tpm)
            assert response.status_code == 201
            
            data = response.json()
            assert "id" in data
            assert data["TPM"] == "TEST_CREATE_TPM"
            assert data["description"] == "Test TPM for creation"
            assert data["A"] == 150
            assert data["B"] == 250
            assert data["H"] == 75
            assert data["variant"] == "v1.0"
            assert data["version"] == 1
            assert data["packType"] == "box"
            assert data["comment"] == "Test comment"
            
            # Verify timestamps are set
            assert "createdTimestamp" in data
            assert "updatedTimestamp" in data
            
            created_id = data["id"]
            
            # Clean up - delete the created TPM
            delete_response = await ac.delete(f"/delete_tpm/{created_id}")
            assert delete_response.status_code == 204

    @pytest.mark.asyncio
    async def test_create_tpm_minimal_data(self):
        """Test creating TPM with minimal required data."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            test_tpm = {
                "TPM": "TEST_MINIMAL_TPM"
            }
            
            response = await ac.post("/create_tpm", json=test_tpm)
            assert response.status_code == 201
            
            data = response.json()
            assert data["TPM"] == "TEST_MINIMAL_TPM"
            assert data["version"] == 1  # Default value
            
            created_id = data["id"]
            
            # Clean up
            delete_response = await ac.delete(f"/delete_tpm/{created_id}")
            assert delete_response.status_code == 204

    @pytest.mark.asyncio
    async def test_create_tpm_invalid_data(self):
        """Test creating TPM with invalid data."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Missing required TPM field
            invalid_tpm = {
                "description": "Missing TPM name"
            }
            
            response = await ac.post("/create_tpm", json=invalid_tpm)
            assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_tpm_crud_full_workflow(self):
        """Test complete CRUD workflow for TPM configuration."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test data for a new TPM
            test_tpm = {
                "TPM": "TEST_CRUD_WORKFLOW_TPM",
                "description": "Full workflow test",
                "A": 100,
                "B": 200,
                "H": 50,
                "variant": "v1.0",
                "version": 1,
                "packType": "container",
                "comment": "Initial comment"
            }
            
            # 1. CREATE - Create a new TPM
            create_response = await ac.post("/create_tpm", json=test_tpm)
            assert create_response.status_code == 201
            created_data = create_response.json()
            created_id = created_data["id"]
            
            assert created_data["TPM"] == "TEST_CRUD_WORKFLOW_TPM"
            assert created_data["description"] == "Full workflow test"
            assert created_data["A"] == 100
            assert created_data["B"] == 200
            assert created_data["H"] == 50
            
            # 2. READ - Verify the TPM exists by getting it by ID
            get_response = await ac.get(f"/get_tpm_by_id/{created_id}")
            assert get_response.status_code == 200
            get_data = get_response.json()
            assert get_data["id"] == created_id
            assert get_data["TPM"] == "TEST_CRUD_WORKFLOW_TPM"
            
            # 3. READ - Verify it appears in the list
            list_response = await ac.get("/get_tpm_config?tpmName=TEST_CRUD_WORKFLOW_TPM")
            assert list_response.status_code == 200
            list_data = list_response.json()
            assert len(list_data["tpms"]) == 1
            assert list_data["tpms"][0]["id"] == created_id
            
            # 4. UPDATE - Update the TPM
            updated_tpm = {
                "TPM": "TEST_CRUD_WORKFLOW_TPM_UPDATED",
                "description": "Updated workflow test",
                "A": 150,
                "B": 250,
                "H": 75,
                "variant": "v2.0",
                "version": 2,
                "packType": "box",
                "comment": "Updated comment"
            }
            
            update_response = await ac.put(f"/update_tpm/{created_id}", json=updated_tpm)
            assert update_response.status_code == 200
            updated_data = update_response.json()
            
            assert updated_data["id"] == created_id
            assert updated_data["TPM"] == "TEST_CRUD_WORKFLOW_TPM_UPDATED"
            assert updated_data["description"] == "Updated workflow test"
            assert updated_data["A"] == 150
            assert updated_data["B"] == 250
            assert updated_data["H"] == 75
            assert updated_data["variant"] == "v2.0"
            assert updated_data["version"] == 2
            
            # 5. READ - Verify the update
            verify_response = await ac.get(f"/get_tpm_by_id/{created_id}")
            assert verify_response.status_code == 200
            verify_data = verify_response.json()
            assert verify_data["TPM"] == "TEST_CRUD_WORKFLOW_TPM_UPDATED"
            assert verify_data["description"] == "Updated workflow test"
            
            # 6. DELETE - Delete the TPM
            delete_response = await ac.delete(f"/delete_tpm/{created_id}")
            assert delete_response.status_code == 204
            
            # 7. VERIFY DELETE - Ensure it's gone
            get_deleted_response = await ac.get(f"/get_tpm_by_id/{created_id}")
            assert get_deleted_response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_tpm_nonexistent(self):
        """Test updating a non-existent TPM."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            update_data = {
                "TPM": "NON_EXISTENT_TPM",
                "description": "This should fail"
            }
            
            response = await ac.put("/update_tpm/99999", json=update_data)
            assert response.status_code == 404
            error_data = response.json()
            assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_update_tpm_invalid_data(self):
        """Test updating TPM with invalid data."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # First get an existing TPM ID
            all_response = await ac.get("/get_tpm_config")
            all_data = all_response.json()
            
            if len(all_data["tpms"]) > 0:
                existing_id = all_data["tpms"][0]["id"]
                
                # Try to update with invalid data (missing required field)
                invalid_data = {
                    "description": "Missing TPM name"
                    # Missing "TPM" field which is required
                }
                
                response = await ac.put(f"/update_tpm/{existing_id}", json=invalid_data)
                assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_delete_tpm_nonexistent(self):
        """Test deleting a non-existent TPM."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/delete_tpm/99999")
            assert response.status_code == 404
            error_data = response.json()
            assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_tpm_data_types_and_validation(self):
        """Test TPM data type validation and edge cases."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test with various data types
            test_tpm = {
                "TPM": "TEST_DATA_TYPES_TPM",
                "description": "Testing data types",
                "A": 0,  # Edge case: zero dimension
                "B": 1,  # Edge case: minimum positive
                "H": 999999,  # Edge case: large number
                "variant": "",  # Edge case: empty string
                "version": 1,
                "packType": None  # Edge case: null value
            }
            
            response = await ac.post("/create_tpm", json=test_tpm)
            assert response.status_code == 201
            
            data = response.json()
            assert data["A"] == 0
            assert data["B"] == 1
            assert data["H"] == 999999
            assert data["variant"] == ""
            assert data["packType"] is None
            
            created_id = data["id"]
            
            # Clean up
            delete_response = await ac.delete(f"/delete_tpm/{created_id}")
            assert delete_response.status_code == 204

    @pytest.mark.asyncio
    async def test_tpm_response_structure(self):
        """Test that TPM responses have the correct structure."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test list response structure
            response = await ac.get("/get_tpm_config")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, dict)
            assert "tpms" in data
            assert isinstance(data["tpms"], list)
            
            if len(data["tpms"]) > 0:
                tpm = data["tpms"][0]
                
                # Check all expected fields are present
                expected_fields = [
                    "id", "TPM", "drawDieline", "drawCombination", "A", "B", "H",
                    "variant", "version", "variablesList", "createdBy", "createdAt",
                    "modifiedBy", "modifiedAt", "packType", "description", "comment",
                    "panelList", "createdTimestamp", "updatedTimestamp"
                ]
                
                for field in expected_fields:
                    assert field in tpm, f"Field {field} missing from TPM response"
                
                # Check required field types
                assert isinstance(tpm["id"], int)
                assert isinstance(tpm["TPM"], str)
                assert isinstance(tpm["version"], int)

    @pytest.mark.asyncio
    async def test_tpm_alias_handling(self):
        """Test that TPM field aliases work correctly."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Create TPM using both alias and non-alias field names
            test_tpm = {
                "TPM": "TEST_ALIAS_TPM",  # Using alias
                "drawDieline": "yes",  # Using alias
                "A": 100,  # Using alias
                "description": "Testing aliases",  # Non-alias field
                "packType": "container"  # Using alias
            }
            
            response = await ac.post("/create_tpm", json=test_tpm)
            assert response.status_code == 201
            
            data = response.json()
            # Response should use aliases in field names
            assert data["TPM"] == "TEST_ALIAS_TPM"
            assert data["drawDieline"] == "yes"
            assert data["A"] == 100
            assert data["packType"] == "container"
            
            created_id = data["id"]
            
            # Clean up
            delete_response = await ac.delete(f"/delete_tpm/{created_id}")
            assert delete_response.status_code == 204


class TestTpmErrorHandling:
    """Test TPM error handling and edge cases"""

    @pytest.mark.asyncio
    async def test_invalid_tpm_id_format(self):
        """Test handling of invalid TPM ID formats."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test non-numeric ID
            response = await ac.get("/get_tpm_by_id/not_a_number")
            assert response.status_code == 422  # Validation error
            
            # Test negative ID
            response = await ac.get("/get_tpm_by_id/-1")
            assert response.status_code == 404  # Not found (could be 422 depending on implementation)

    @pytest.mark.asyncio
    async def test_malformed_json_requests(self):
        """Test handling of malformed JSON in requests."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Test invalid JSON
            response = await ac.post(
                "/create_tpm",
                content='{"TPM": "test", invalid json}',
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 422  # JSON parsing error

    @pytest.mark.asyncio
    async def test_empty_request_body(self):
        """Test handling of empty request bodies."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/create_tpm", json={})
            assert response.status_code == 422  # Missing required fields