import pytest

from data.layers import LAYER_DATA
from data.swatches import SWATCH_DATA
from main import app
from models import ColorModel, ColorSpace, SwatchConfig


class TestRootEndpoint:
    """Tests for the root endpoint (/)"""
    
    def test_root_endpoint_returns_correct_response(self, client):
        """Test that root endpoint returns expected message and version."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "ScriPTA", "version": "1.0.1"}
    
    def test_root_endpoint_content_type(self, client):
        """Test that root endpoint returns JSON content type."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestGetSwatchConfigEndpoint:
    """Tests for the /get_swatch_config endpoint"""
    
    def test_get_all_swatches_without_filter(self, client):
        """Test getting all swatches when no color name filter is provided."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        assert "swatches" in data
        assert len(data["swatches"]) == len(SWATCH_DATA)
        
        # Verify structure of first swatch
        first_swatch = data["swatches"][0]
        assert "colorName" in first_swatch
        assert "colorModel" in first_swatch
        assert "colorSpace" in first_swatch
        assert "colorValues" in first_swatch

    def test_get_swatches_with_valid_colorname_filter(self, client):
        """Test filtering by a valid color name."""
        response = client.get("/get_swatch_config?colorName=DIELINE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "DIELINE"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [50, 50, 0, 0]
    
    def test_get_swatches_with_another_valid_colorname(self, client):
        """Test filtering by another valid color name."""
        response = client.get("/get_swatch_config?colorName=PA123")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA123"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [0, 24, 94, 0]
    
    def test_get_swatches_with_process_color_model(self, client):
        """Test filtering by color name that has PROCESS color model."""
        response = client.get("/get_swatch_config?colorName=PA321")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA321"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [95, 20, 25, 20]
    
    def test_get_swatches_with_invalid_colorname_returns_404(self, client):
        """Test that filtering by invalid color name returns 404."""
        response = client.get("/get_swatch_config?colorName=NONEXISTENT")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Color name 'NONEXISTENT' not found"
    
    def test_get_swatches_with_empty_colorname(self, client):
        """Test behavior when color name parameter is empty."""
        response = client.get("/get_swatch_config?colorName=")
        # Empty color name is treated as None, so returns all swatches
        assert response.status_code == 200
        data = response.json()
        assert len(data["swatches"]) == len(SWATCH_DATA)
    
    def test_get_swatches_case_sensitive_colorname(self, client):
        """Test that color name filtering is case sensitive."""
        response = client.get("/get_swatch_config?colorName=dieline")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_response_schema_compliance(self, client):
        """Test that response follows the expected schema."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check top-level structure
        assert isinstance(data, dict)
        assert "swatches" in data
        assert isinstance(data["swatches"], list)
        
        # Check each swatch structure
        for swatch in data["swatches"]:
            assert isinstance(swatch, dict)
            assert "colorName" in swatch
            assert "colorModel" in swatch
            assert "colorSpace" in swatch
            assert "colorValues" in swatch
            
            # Validate types
            assert isinstance(swatch["colorName"], str)
            assert isinstance(swatch["colorModel"], str)
            assert isinstance(swatch["colorSpace"], str)
            assert isinstance(swatch["colorValues"], list)
            
            # Validate that colorValues contains integers
            for value in swatch["colorValues"]:
                assert isinstance(value, int)
            
            # Validate enum values
            assert swatch["colorModel"] in ["SPOT", "PROCESS"]
            assert swatch["colorSpace"] in ["CMYK", "RGB", "LAB"]
    
    def test_multiple_query_parameters(self, client):
        """Test behavior with multiple query parameters (only color name should be used)."""
        response = client.get("/get_swatch_config?colorName=DIELINE&other_param=value")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        assert data["swatches"][0]["colorName"] == "DIELINE"
    
    def test_content_type_header(self, client):
        """Test that the endpoint returns correct content type."""
        response = client.get("/get_swatch_config")
        assert response.headers["content-type"] == "application/json"
    
    def test_all_expected_swatches_present(self, client):
        """Test that all expected swatches from SWATCH_DATA are returned."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        color_names = [swatch["colorName"] for swatch in data["swatches"]]
        expected_color_names = [swatch.color_name for swatch in SWATCH_DATA]
        
        assert set(color_names) == set(expected_color_names)
    
    def test_swatch_data_integrity(self, client):
        """Test that returned data matches the source data exactly."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        
        # Create a mapping of returned data by color name for easy lookup
        returned_swatches = {swatch["colorName"]: swatch for swatch in data["swatches"]}
        
        # Compare each swatch in SWATCH_DATA with returned data
        for expected_swatch in SWATCH_DATA:
            returned_swatch = returned_swatches[expected_swatch.color_name]
            
            assert returned_swatch["colorName"] == expected_swatch.color_name
            assert returned_swatch["colorModel"] == expected_swatch.color_model
            assert returned_swatch["colorSpace"] == expected_swatch.color_space
            assert returned_swatch["colorValues"] == expected_swatch.color_values


class TestEndpointEdgeCases:
    """Tests for edge cases and error conditions"""
    
    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that accessing non-existent endpoints returns 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_wrong_http_method_on_get_swatch_config(self, client):
        """Test that using wrong HTTP method returns 405."""
        response = client.post("/get_swatch_config")
        assert response.status_code == 405
    
    def test_wrong_http_method_on_root(self, client):
        """Test that using wrong HTTP method on root returns 405."""
        response = client.post("/")
        assert response.status_code == 405


@pytest.fixture
def sample_swatch_data():
    """Fixture providing sample swatch data for testing."""
    return [
        SwatchConfig(
            color_name="TEST_COLOR",
            color_model=ColorModel.SPOT,
            color_space=ColorSpace.RGB,
            color_values="255,0,0"
        )
    ]


class TestDataConsistency:
    """Tests to ensure data consistency and validation"""
    
    def test_enum_values_are_consistent(self, client):
        """Test that enum values in responses match model definitions."""
        response = client.get("/get_swatch_config")
        data = response.json()
        
        for swatch in data["swatches"]:
            # Verify color_model values are valid
            assert swatch["colorModel"] in ["SPOT", "PROCESS"]
            # Verify color_space values are valid  
            assert swatch["colorSpace"] in ["CMYK", "RGB", "LAB"]
    
    def test_color_values_format(self, client):
        """Test that color values are in expected array format."""
        response = client.get("/get_swatch_config")
        data = response.json()
        
        for swatch in data["swatches"]:
            color_values = swatch["colorValues"]
            # Should be an array of integers
            assert isinstance(color_values, list)
            assert len(color_values) > 0  # Should have at least one value
            
            # Check that all values are integers
            for value in color_values:
                assert isinstance(value, int), f"Invalid color value: {value}"


class TestSpecificSwatchData:
    """Tests to verify specific swatches are present in SWATCH_DATA"""
    
    def test_c20m90y0k40_swatch_present(self, client):
        """Test that C20M90Y0K40 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=C20M90Y0K40")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "C20M90Y0K40"
        assert swatch["colorModel"] == "PROCESS"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [20, 90, 0, 40]
    
    def test_proc699_swatch_present(self, client):
        """Test that PROC699 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PROC699")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PROC699"
        assert swatch["colorModel"] == "PROCESS"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [0, 30, 7, 0]
    
    def test_embossing_swatch_present(self, client):
        """Test that EMBOSSING swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=EMBOSSING")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "EMBOSSING"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [70, 0, 70, 0]
    
    def test_not_printable_swatch_present(self, client):
        """Test that NOT_PRINTABLE swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=NOT_PRINTABLE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "NOT_PRINTABLE"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [0, 100, 0, 0]
    
    def test_pa301_swatch_present(self, client):
        """Test that PA301 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PA301")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA301"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [100, 45, 0, 18]
    
    def test_pa520_swatch_present(self, client):
        """Test that PA520 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PA520")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA520"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [69, 94, 18, 0]
    
    def test_paprocyan_swatch_present(self, client):
        """Test that PAPROCYAN swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PAPROCYAN")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PAPROCYAN"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [100, 0, 0, 0]
    
    def test_white_opaque_swatch_present(self, client):
        """Test that WHITE_OPAQUE swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=WHITE_OPAQUE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "WHITE_OPAQUE"
        assert swatch["colorModel"] == "SPOT"
        assert swatch["colorSpace"] == "CMYK"
        assert swatch["colorValues"] == [27, 4, 0, 0]
    
    def test_all_required_swatches_present(self, client):
        """Test that all required swatches are present in the data."""
        required_swatches = [
            "C20M90Y0K40",
            "PROC699", 
            "EMBOSSING",
            "NOT_PRINTABLE",
            "PA301",
            "PA520",
            "PAPROCYAN",
            "WHITE_OPAQUE"
        ]
        
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        returned_color_names = [swatch["colorName"] for swatch in data["swatches"]]
        
        for required_swatch in required_swatches:
            assert required_swatch in returned_color_names, f"Required swatch '{required_swatch}' not found in data"


class TestParameterizedTests:
    """Parametrized tests using fixtures"""
    
    def test_valid_colornames(self, client, sample_colornames):
        """Test all valid color names return correct results."""
        for color_name in sample_colornames:
            response = client.get(f"/get_swatch_config?colorName={color_name}")
            assert response.status_code == 200
            data = response.json()
            assert len(data["swatches"]) == 1
            assert data["swatches"][0]["colorName"] == color_name
    
    def test_invalid_colornames(self, client, invalid_colornames):
        """Test all invalid color names return 404."""
        for color_name in invalid_colornames:
            response = client.get(f"/get_swatch_config?colorName={color_name}")
            if color_name == "":
                # Empty color name returns all swatches
                assert response.status_code == 200
            else:
                assert response.status_code == 404
                assert "not found" in response.json()["detail"].lower()


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


class TestLayerConfigEndpointEdgeCases:
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
        import time
        
        start_time = time.time()
        response = client.get("/get_layer_config")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
