"""
Tests specifically for the layer config endpoint (/get_layer_config).
This module contains comprehensive tests for the layer configuration API endpoint.
"""

import time

import pytest

from ..main import app
from ..src.data.layers import LAYER_DATA


class TestGetLayerConfigEndpoint:
    """Tests for the /get_layer_config endpoint"""
    
    def test_get_all_layer_configs_without_filter(self, client):
        """Test getting all layer configurations when no config name filter is provided."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(LAYER_DATA)
        
        # Verify structure of first config
        first_config = data[0]
        assert "configName" in first_config
        assert "layers" in first_config
        assert isinstance(first_config["layers"], list)
        assert len(first_config["layers"]) > 0
        
        # Verify structure of first layer in first config
        first_layer = first_config["layers"][0]
        assert "name" in first_layer
        assert "locked" in first_layer
        assert "print" in first_layer
        assert "color" in first_layer
    
    def test_get_layer_config_with_valid_config_name_default(self, client):
        """Test filtering by the 'default' config name."""
        response = client.get("/get_layer_config?configName=default")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        
        config = data[0]
        assert config["configName"] == "default"
        assert len(config["layers"]) == 9  # default config has 9 layers
        
        # Verify specific layer details for default config
        layer_names = [layer["name"] for layer in config["layers"]]
        expected_layer_names = ["DIELINE", "TECHNICAL", "BRAILLE_EMB", "TEXT", 
                               "ACF_HRL", "ACF_LRA_VARNISH", "DESIGN", "INFOBOX", "GUIDES"]
        assert layer_names == expected_layer_names
    
    def test_get_layer_config_with_valid_config_name_foldingbox(self, client):
        """Test filtering by the 'FoldingBox' config name."""
        response = client.get("/get_layer_config?configName=FoldingBox")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        
        config = data[0]
        assert config["configName"] == "FoldingBox"
        assert len(config["layers"]) == 9  # FoldingBox config has 9 layers
    
    def test_get_layer_config_with_valid_config_name_label(self, client):
        """Test filtering by the 'Label' config name."""
        response = client.get("/get_layer_config?configName=Label")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        
        config = data[0]
        assert config["configName"] == "Label"
        assert len(config["layers"]) == 4  # Label config has 4 layers
        
        # Verify specific layer details for Label config
        layer_names = [layer["name"] for layer in config["layers"]]
        expected_layer_names = ["TEXT", "DESIGN", "GUIDES", "DIELINE"]
        assert layer_names == expected_layer_names
    
    def test_get_layer_config_with_valid_config_name_tpm(self, client):
        """Test filtering by the 'TPM' config name."""
        response = client.get("/get_layer_config?configName=TPM")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        
        config = data[0]
        assert config["configName"] == "TPM"
        assert len(config["layers"]) == 3  # TPM config has 3 layers
        
        # Verify specific layer details for TPM config
        layer_names = [layer["name"] for layer in config["layers"]]
        expected_layer_names = ["GUIDES", "PANEL", "DIELINE"]
        assert layer_names == expected_layer_names
    
    def test_get_layer_config_with_invalid_config_name_returns_404(self, client):
        """Test that filtering by invalid config name returns 404."""
        response = client.get("/get_layer_config?configName=NONEXISTENT")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Config name 'NONEXISTENT' not found"
    
    def test_get_layer_config_with_empty_config_name(self, client):
        """Test behavior when config name parameter is empty."""
        response = client.get("/get_layer_config?configName=")
        # Empty config name is treated as None, so returns all configs
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(LAYER_DATA)
    
    def test_get_layer_config_case_sensitive_config_name(self, client):
        """Test that config name filtering is case sensitive."""
        response = client.get("/get_layer_config?configName=default")  # lowercase 'd'
        assert response.status_code == 200  # This should work since the actual config is lowercase
        
        response = client.get("/get_layer_config?configName=DEFAULT")  # uppercase
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestLayerConfigResponseValidation:
    """Tests for validating the response structure and data integrity"""
    
    def test_layer_config_response_schema_compliance(self, client):
        """Test that response follows the expected schema."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check top-level structure
        assert isinstance(data, list)
        
        # Check each config structure
        for config in data:
            assert isinstance(config, dict)
            assert "configName" in config
            assert "layers" in config
            
            # Validate types
            assert isinstance(config["configName"], str)
            assert isinstance(config["layers"], list)
            
            # Check each layer structure
            for layer in config["layers"]:
                assert isinstance(layer, dict)
                assert "name" in layer
                assert "locked" in layer
                assert "print" in layer
                assert "color" in layer
                
                # Validate types
                assert isinstance(layer["name"], str)
                assert isinstance(layer["locked"], bool)
                assert isinstance(layer["print"], bool)
                assert isinstance(layer["color"], str)
                
                # Validate enum values
                valid_layer_names = ["DIELINE", "TECHNICAL", "BRAILLE_EMB", "TEXT", 
                                   "ACF_HRL", "ACF_LRA_VARNISH", "DESIGN", "INFOBOX", "GUIDES", "PANEL"]
                valid_colors = ["GOLD", "TEAL", "FIESTA", "LIGHT_BLUE", "YELLOW", 
                              "GREEN", "RED", "LAVENDER", "GRAY", "BLUE"]
                assert layer["name"] in valid_layer_names
                assert layer["color"] in valid_colors
    
    def test_layer_config_multiple_query_parameters(self, client):
        """Test behavior with multiple query parameters (only config name should be used)."""
        response = client.get("/get_layer_config?configName=default&other_param=value")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["configName"] == "default"
    
    def test_layer_config_content_type_header(self, client):
        """Test that the endpoint returns correct content type."""
        response = client.get("/get_layer_config")
        assert response.headers["content-type"] == "application/json"
    
    def test_all_expected_layer_configs_present(self, client):
        """Test that all expected layer configs from LAYER_DATA are returned."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        
        data = response.json()
        config_names = [config["configName"] for config in data]
        expected_config_names = [config.config_name for config in LAYER_DATA]
        
        assert set(config_names) == set(expected_config_names)
    
    def test_layer_config_data_integrity(self, client):
        """Test that returned data matches the source data exactly."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        
        data = response.json()
        
        # Create a mapping of returned data by config name for easy lookup
        returned_configs = {config["configName"]: config for config in data}
        
        # Compare each config in LAYER_DATA with returned data
        for expected_config in LAYER_DATA:
            returned_config = returned_configs[expected_config.config_name]
            
            assert returned_config["configName"] == expected_config.config_name
            assert len(returned_config["layers"]) == len(expected_config.layers)
            
            # Create mappings of layers by name for comparison
            returned_layers = {layer["name"]: layer for layer in returned_config["layers"]}
            
            for expected_layer in expected_config.layers:
                returned_layer = returned_layers[expected_layer.name.value]
                
                assert returned_layer["name"] == expected_layer.name.value
                assert returned_layer["locked"] == expected_layer.locked
                assert returned_layer["print"] == expected_layer.print
                assert returned_layer["color"] == expected_layer.color.value


class TestLayerConfigSpecificBehaviors:
    """Tests for specific layer configuration behaviors and properties"""
    
    def test_layer_config_specific_layer_properties(self, client):
        """Test specific layer properties in different configurations."""
        response = client.get("/get_layer_config?configName=default")
        assert response.status_code == 200
        
        data = response.json()
        config = data[0]
        
        # Find specific layers and test their properties
        dieline_layer = next(layer for layer in config["layers"] if layer["name"] == "DIELINE")
        assert dieline_layer["locked"] == True
        assert dieline_layer["print"] == True
        assert dieline_layer["color"] == "GOLD"
        
        guides_layer = next(layer for layer in config["layers"] if layer["name"] == "GUIDES")
        assert guides_layer["locked"] == True
        assert guides_layer["print"] == False  # GUIDES layer doesn't print
        assert guides_layer["color"] == "GRAY"
        
        text_layer = next(layer for layer in config["layers"] if layer["name"] == "TEXT")
        assert text_layer["locked"] == False
        assert text_layer["print"] == True
        assert text_layer["color"] == "LIGHT_BLUE"
    
    def test_layer_config_different_config_variations(self, client):
        """Test that different configs have different layer arrangements."""
        # Get all configs
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        data = response.json()
        
        # Find specific configs
        default_config = next(c for c in data if c["configName"] == "default")
        label_config = next(c for c in data if c["configName"] == "Label")
        tpm_config = next(c for c in data if c["configName"] == "TPM")
        
        # Verify they have different layer counts
        assert len(default_config["layers"]) == 9
        assert len(label_config["layers"]) == 4
        assert len(tpm_config["layers"]) == 3
        
        # Verify TPM config has PANEL layer but others don't
        tpm_layer_names = [layer["name"] for layer in tpm_config["layers"]]
        default_layer_names = [layer["name"] for layer in default_config["layers"]]
        label_layer_names = [layer["name"] for layer in label_config["layers"]]
        
        assert "PANEL" in tpm_layer_names
        assert "PANEL" not in default_layer_names
        assert "PANEL" not in label_layer_names
    
    def test_layer_config_locked_vs_unlocked_layers(self, client):
        """Test that locked and unlocked layers are correctly identified."""
        response = client.get("/get_layer_config?configName=default")
        assert response.status_code == 200
        
        data = response.json()
        config = data[0]
        
        locked_layers = [layer for layer in config["layers"] if layer["locked"]]
        unlocked_layers = [layer for layer in config["layers"] if not layer["locked"]]
        
        # Verify we have both locked and unlocked layers
        assert len(locked_layers) > 0
        assert len(unlocked_layers) > 0
        
        # Check specific layers that should be locked
        locked_layer_names = [layer["name"] for layer in locked_layers]
        assert "DIELINE" in locked_layer_names
        assert "GUIDES" in locked_layer_names
        assert "INFOBOX" in locked_layer_names
    
    def test_layer_config_printable_vs_non_printable_layers(self, client):
        """Test that printable and non-printable layers are correctly identified."""
        response = client.get("/get_layer_config?configName=default")
        assert response.status_code == 200
        
        data = response.json()
        config = data[0]
        
        printable_layers = [layer for layer in config["layers"] if layer["print"]]
        non_printable_layers = [layer for layer in config["layers"] if not layer["print"]]
        
        # Verify we have printable layers
        assert len(printable_layers) > 0
        
        # Check that GUIDES layer is not printable (this is typical for guides)
        guides_layer = next((layer for layer in config["layers"] if layer["name"] == "GUIDES"), None)
        assert guides_layer is not None
        assert guides_layer["print"] == False


class TestLayerConfigEdgeCases:
    """Tests for edge cases and error conditions for layer config endpoint"""
    
    def test_wrong_http_method_on_get_layer_config(self, client):
        """Test that using wrong HTTP method returns 405."""
        response = client.post("/get_layer_config")
        assert response.status_code == 405
        
        response = client.put("/get_layer_config")
        assert response.status_code == 405
        
        response = client.delete("/get_layer_config")
        assert response.status_code == 405
    
    def test_layer_config_with_special_characters_in_config_name(self, client):
        """Test behavior with special characters in config name."""
        special_names = ["config@name", "config name", "config/name", "config?name"]
        
        for name in special_names:
            response = client.get(f"/get_layer_config?configName={name}")
            assert response.status_code == 404
            assert "not found" in response.json()["detail"]
    
    def test_layer_config_performance_with_all_configs(self, client):
        """Test that endpoint responds quickly even with all configs."""        
        start_time = time.time()
        response = client.get("/get_layer_config")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
    
    def test_layer_config_with_numeric_config_name(self, client):
        """Test behavior with numeric config name."""
        response = client.get("/get_layer_config?configName=123")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_layer_config_with_very_long_config_name(self, client):
        """Test behavior with very long config name."""
        long_name = "a" * 1000
        response = client.get(f"/get_layer_config?configName={long_name}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestLayerConfigParameterized:
    """Parameterized tests for layer config endpoint"""
    
    @pytest.mark.parametrize("config_name", ["default", "FoldingBox", "Label", "TPM"])
    def test_valid_config_names(self, client, config_name):
        """Test all valid config names return 200 and correct data."""
        response = client.get(f"/get_layer_config?configName={config_name}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["configName"] == config_name
    
    @pytest.mark.parametrize("invalid_name", ["NONEXISTENT", "INVALID", "NOT_FOUND", "DEFAULT", "foldingbox"])
    def test_invalid_config_names(self, client, invalid_name):
        """Test all invalid config names return 404."""
        response = client.get(f"/get_layer_config?configName={invalid_name}")
        if invalid_name == "":
            # Empty config name returns all configs
            assert response.status_code == 200
        else:
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.parametrize("layer_name", ["DIELINE", "TECHNICAL", "BRAILLE_EMB", "TEXT", 
                                           "ACF_HRL", "ACF_LRA_VARNISH", "DESIGN", "INFOBOX", "GUIDES", "PANEL"])
    def test_all_layer_names_present_somewhere(self, client, layer_name):
        """Test that each layer name appears in at least one configuration."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        data = response.json()
        
        # Check if layer_name appears in any configuration
        found = False
        for config in data:
            for layer in config["layers"]:
                if layer["name"] == layer_name:
                    found = True
                    break
            if found:
                break
        
        assert found, f"Layer '{layer_name}' was not found in any configuration"
    
    @pytest.mark.parametrize("color", ["GOLD", "TEAL", "FIESTA", "LIGHT_BLUE", "YELLOW", 
                                      "GREEN", "RED", "LAVENDER", "GRAY", "BLUE"])
    def test_all_colors_used_somewhere(self, client, color):
        """Test that each color is used in at least one layer."""
        response = client.get("/get_layer_config")
        assert response.status_code == 200
        data = response.json()
        
        # Check if color appears in any layer
        found = False
        for config in data:
            for layer in config["layers"]:
                if layer["color"] == color:
                    found = True
                    break
            if found:
                break
        
        assert found, f"Color '{color}' was not found in any layer"


class TestLayerConfigCRUD:
    """Test layer configuration CRUD operations"""

    @pytest.mark.asyncio
    async def test_layer_config_crud_full_workflow(self, async_client):
        """Test complete CRUD workflow for layer configuration."""
        # Test data for a new layer configuration set
        test_layer_config = {
            "config_name": "TEST_CRUD_CONFIG",
            "layers": [
                {
                    "name": "DIELINE",
                    "locked": False,
                    "print": True,
                    "color": "GOLD"
                },
                {
                    "name": "TEXT",
                    "locked": True,
                    "print": True,
                    "color": "BLUE"
                },
                {
                    "name": "DESIGN",
                    "locked": False,
                    "print": True,
                    "color": "RED"
                }
            ]
        }
        
        # 1. Create a new layer configuration
        create_response = await async_client.post("/create_layer_config", json=test_layer_config)
        assert create_response.status_code == 200
        created_data = create_response.json()
        assert created_data["config_name"] == "TEST_CRUD_CONFIG"
        assert len(created_data["layers"]) == 3
        assert created_data["layers"][0]["name"] == "DIELINE"
        assert created_data["layers"][0]["locked"] is False
        assert created_data["layers"][0]["print"] is True
        assert created_data["layers"][0]["color"] == "GOLD"
        
        # 2. Verify the config exists by getting it
        get_response = await async_client.get("/get_layer_config?configName=TEST_CRUD_CONFIG")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert len(get_data) == 1
        assert get_data[0]["configName"] == "TEST_CRUD_CONFIG"
        assert len(get_data[0]["layers"]) == 3
        
        # 3. Update the layer configuration
        updated_config = {
            "config_name": "TEST_CRUD_CONFIG_UPDATED",
            "layers": [
                {
                    "name": "DIELINE",
                    "locked": True,
                    "print": False,
                    "color": "TEAL"
                },
                {
                    "name": "GUIDES",
                    "locked": False,
                    "print": True,
                    "color": "GRAY"
                }
            ]
        }
        update_response = await async_client.put("/update_layer_config/TEST_CRUD_CONFIG", json=updated_config)
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["config_name"] == "TEST_CRUD_CONFIG_UPDATED"
        assert len(updated_data["layers"]) == 2
        assert updated_data["layers"][0]["locked"] is True
        assert updated_data["layers"][0]["print"] is False
        assert updated_data["layers"][0]["color"] == "TEAL"
        
        # 4. Verify the update by getting the config with new name
        get_updated_response = await async_client.get("/get_layer_config?configName=TEST_CRUD_CONFIG_UPDATED")
        assert get_updated_response.status_code == 200
        get_updated_data = get_updated_response.json()
        assert len(get_updated_data) == 1
        assert get_updated_data[0]["configName"] == "TEST_CRUD_CONFIG_UPDATED"
        assert len(get_updated_data[0]["layers"]) == 2
        
        # 5. Delete the configuration
        delete_response = await async_client.delete("/delete_layer_config/TEST_CRUD_CONFIG_UPDATED")
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert "deleted successfully" in delete_data["message"]
        
        # 6. Verify the configuration is deleted
        get_deleted_response = await async_client.get("/get_layer_config?configName=TEST_CRUD_CONFIG_UPDATED")
        assert get_deleted_response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_layer_config_success(self, async_client):
        """Test successful layer configuration creation."""
        test_config = {
            "config_name": "CREATE_TEST_CONFIG",
            "layers": [
                {
                    "name": "TEXT",
                    "locked": False,
                    "print": True,
                    "color": "BLUE"
                }
            ]
        }
        
        # Create configuration
        response = await async_client.post("/create_layer_config", json=test_config)
        assert response.status_code == 200
        data = response.json()
        assert data["config_name"] == "CREATE_TEST_CONFIG"
        assert len(data["layers"]) == 1
        
        # Cleanup - delete the created configuration
        await async_client.delete("/delete_layer_config/CREATE_TEST_CONFIG")

    @pytest.mark.asyncio
    async def test_create_layer_config_duplicate_error(self, async_client):
        """Test creating duplicate layer configuration returns 409 error."""
        # Try to create a configuration with existing name (default exists in test data)
        test_config = {
            "config_name": "default",
            "layers": [
                {
                    "name": "TEXT",
                    "locked": False,
                    "print": True,
                    "color": "BLUE"
                }
            ]
        }
        
        response = await async_client.post("/create_layer_config", json=test_config)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_layer_config_invalid_data(self, async_client):
        """Test creating layer configuration with invalid data returns 422 error."""
        # Missing required fields
        invalid_config = {
            "config_name": "INVALID_CONFIG"
            # Missing layers field
        }
        
        response = await async_client.post("/create_layer_config", json=invalid_config)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_layer_config_success(self, async_client):
        """Test successful layer configuration update."""
        # First create a configuration to update
        initial_config = {
            "config_name": "UPDATE_TEST_CONFIG",
            "layers": [
                {
                    "name": "DIELINE",
                    "locked": False,
                    "print": True,
                    "color": "GOLD"
                }
            ]
        }
        
        create_response = await async_client.post("/create_layer_config", json=initial_config)
        assert create_response.status_code == 200
        
        # Update the configuration
        updated_config = {
            "config_name": "UPDATE_TEST_CONFIG_MODIFIED",
            "layers": [
                {
                    "name": "TEXT",
                    "locked": True,
                    "print": False,
                    "color": "RED"
                },
                {
                    "name": "DESIGN",
                    "locked": False,
                    "print": True,
                    "color": "GREEN"
                }
            ]
        }
        
        response = await async_client.put("/update_layer_config/UPDATE_TEST_CONFIG", json=updated_config)
        assert response.status_code == 200
        data = response.json()
        assert data["config_name"] == "UPDATE_TEST_CONFIG_MODIFIED"
        assert len(data["layers"]) == 2
        
        # Cleanup
        await async_client.delete("/delete_layer_config/UPDATE_TEST_CONFIG_MODIFIED")

    @pytest.mark.asyncio
    async def test_update_layer_config_not_found(self, async_client):
        """Test updating non-existent layer configuration returns 404 error."""
        updated_config = {
            "config_name": "NONEXISTENT_UPDATED",
            "layers": [
                {
                    "name": "TEXT",
                    "locked": False,
                    "print": True,
                    "color": "BLUE"
                }
            ]
        }
        
        response = await async_client.put("/update_layer_config/NONEXISTENT_CONFIG", json=updated_config)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_delete_layer_config_success(self, async_client):
        """Test successful layer configuration deletion."""
        # First create a configuration to delete
        test_config = {
            "config_name": "DELETE_TEST_CONFIG",
            "layers": [
                {
                    "name": "GUIDES",
                    "locked": False,
                    "print": True,
                    "color": "GRAY"
                }
            ]
        }
        
        create_response = await async_client.post("/create_layer_config", json=test_config)
        assert create_response.status_code == 200
        
        # Delete the configuration
        response = await async_client.delete("/delete_layer_config/DELETE_TEST_CONFIG")
        assert response.status_code == 200
        data = response.json()
        assert "DELETE_TEST_CONFIG" in data["message"]
        assert "deleted successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_delete_layer_config_not_found(self, async_client):
        """Test deleting non-existent layer configuration returns 404 error."""
        response = await async_client.delete("/delete_layer_config/NONEXISTENT_CONFIG")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_layer_config_with_all_layer_types(self, async_client):
        """Test creating configuration with various layer types and properties."""
        comprehensive_config = {
            "config_name": "COMPREHENSIVE_TEST_CONFIG",
            "layers": [
                {
                    "name": "DIELINE",
                    "locked": True,
                    "print": False,
                    "color": "GOLD"
                },
                {
                    "name": "TECHNICAL",
                    "locked": False,
                    "print": True,
                    "color": "TEAL"
                },
                {
                    "name": "BRAILLE_EMB",
                    "locked": True,
                    "print": True,
                    "color": "FIESTA"
                },
                {
                    "name": "TEXT",
                    "locked": False,
                    "print": True,
                    "color": "LIGHT_BLUE"
                },
                {
                    "name": "ACF_HRL",
                    "locked": False,
                    "print": False,
                    "color": "YELLOW"
                },
                {
                    "name": "ACF_LRA_VARNISH",
                    "locked": True,
                    "print": True,
                    "color": "GREEN"
                },
                {
                    "name": "DESIGN",
                    "locked": False,
                    "print": True,
                    "color": "RED"
                },
                {
                    "name": "INFOBOX",
                    "locked": True,
                    "print": False,
                    "color": "LAVENDER"
                },
                {
                    "name": "GUIDES",
                    "locked": False,
                    "print": False,
                    "color": "GRAY"
                }
            ]
        }
        
        response = await async_client.post("/create_layer_config", json=comprehensive_config)
        assert response.status_code == 200
        data = response.json()
        assert data["config_name"] == "COMPREHENSIVE_TEST_CONFIG"
        assert len(data["layers"]) == 9
        
        # Verify all layers are present with correct properties
        layer_dict = {layer["name"]: layer for layer in data["layers"]}
        assert layer_dict["DIELINE"]["locked"] is True
        assert layer_dict["DIELINE"]["print"] is False
        assert layer_dict["DIELINE"]["color"] == "GOLD"
        
        assert layer_dict["TECHNICAL"]["locked"] is False
        assert layer_dict["TECHNICAL"]["print"] is True
        assert layer_dict["TECHNICAL"]["color"] == "TEAL"
        
        # Cleanup
        await async_client.delete("/delete_layer_config/COMPREHENSIVE_TEST_CONFIG")
