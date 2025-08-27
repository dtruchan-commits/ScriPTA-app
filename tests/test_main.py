import pytest
from main import app
from models import SwatchConfig, ColorModel, ColorSpace
from data import SWATCH_DATA


class TestRootEndpoint:
    """Tests for the root endpoint (/)"""
    
    def test_root_endpoint_returns_correct_response(self, client):
        """Test that root endpoint returns expected message and version."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "SwatchWorx API", "version": "1.0.0"}
    
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
        assert "color_model" in first_swatch
        assert "color_space" in first_swatch
        assert "colorValues" in first_swatch
    
    def test_get_swatches_with_valid_colorname_filter(self, client):
        """Test filtering by a valid color name."""
        response = client.get("/get_swatch_config?colorName=DIELINE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "DIELINE"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "50,50,0,0"
    
    def test_get_swatches_with_another_valid_colorname(self, client):
        """Test filtering by another valid color name."""
        response = client.get("/get_swatch_config?colorName=PA123")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA123"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "0,24,94,0"
    
    def test_get_swatches_with_process_color_model(self, client):
        """Test filtering by color name that has PROCESS color model."""
        response = client.get("/get_swatch_config?colorName=PA321")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA321"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "95,20,25,20"
    
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
            assert "color_model" in swatch
            assert "color_space" in swatch
            assert "colorValues" in swatch
            
            # Validate types
            assert isinstance(swatch["colorName"], str)
            assert isinstance(swatch["color_model"], str)
            assert isinstance(swatch["color_space"], str)
            assert isinstance(swatch["colorValues"], str)
            
            # Validate enum values
            assert swatch["color_model"] in ["SPOT", "PROCESS"]
            assert swatch["color_space"] in ["CMYK", "RGB", "LAB"]
    
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
            assert returned_swatch["color_model"] == expected_swatch.color_model
            assert returned_swatch["color_space"] == expected_swatch.color_space
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
            assert swatch["color_model"] in ["SPOT", "PROCESS"]
            # Verify color_space values are valid  
            assert swatch["color_space"] in ["CMYK", "RGB", "LAB"]
    
    def test_colorvalues_format(self, client):
        """Test that color values are in expected comma-separated format."""
        response = client.get("/get_swatch_config")
        data = response.json()
        
        for swatch in data["swatches"]:
            color_values = swatch["colorValues"]
            # Should be comma-separated values
            assert isinstance(color_values, str)
            assert "," in color_values or color_values.isdigit()  # Single value or comma-separated
            
            # Split and check that all parts are numeric
            values = color_values.split(",")
            for value in values:
                assert value.strip().isdigit(), f"Invalid color value: {value}"


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
        assert swatch["color_model"] == "PROCESS"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "20,90,0,40"
    
    def test_proc699_swatch_present(self, client):
        """Test that PROC699 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PROC699")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PROC699"
        assert swatch["color_model"] == "PROCESS"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "0,30,7,0"
    
    def test_embossing_swatch_present(self, client):
        """Test that EMBOSSING swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=EMBOSSING")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "EMBOSSING"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "70,0,70,0"
    
    def test_not_printable_swatch_present(self, client):
        """Test that NOT_PRINTABLE swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=NOT_PRINTABLE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "NOT_PRINTABLE"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "0,100,0,0"
    
    def test_pa301_swatch_present(self, client):
        """Test that PA301 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PA301")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA301"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "100,45,0,18"
    
    def test_pa520_swatch_present(self, client):
        """Test that PA520 swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PA520")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PA520"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "69,94,18,0"
    
    def test_paprocyan_swatch_present(self, client):
        """Test that PAPROCYAN swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=PAPROCYAN")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "PAPROCYAN"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "100,0,0,0"
    
    def test_white_opaque_swatch_present(self, client):
        """Test that WHITE_OPAQUE swatch is present with correct data."""
        response = client.get("/get_swatch_config?colorName=WHITE_OPAQUE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorName"] == "WHITE_OPAQUE"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorValues"] == "27,4,0,0"
    
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
