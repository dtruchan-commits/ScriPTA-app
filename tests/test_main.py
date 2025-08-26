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
        """Test getting all swatches when no colorname filter is provided."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        assert "swatches" in data
        assert len(data["swatches"]) == len(SWATCH_DATA)
        
        # Verify structure of first swatch
        first_swatch = data["swatches"][0]
        assert "colorname" in first_swatch
        assert "color_model" in first_swatch
        assert "color_space" in first_swatch
        assert "colorvalues" in first_swatch
    
    def test_get_swatches_with_valid_colorname_filter(self, client):
        """Test filtering by a valid colorname."""
        response = client.get("/get_swatch_config?colorname=DIELINE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorname"] == "DIELINE"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorvalues"] == "0,50,100,0"
    
    def test_get_swatches_with_another_valid_colorname(self, client):
        """Test filtering by another valid colorname."""
        response = client.get("/get_swatch_config?colorname=PA123")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorname"] == "PA123"
        assert swatch["color_model"] == "SPOT"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorvalues"] == "50,50,50,50"
    
    def test_get_swatches_with_process_color_model(self, client):
        """Test filtering by colorname that has PROCESS color model."""
        response = client.get("/get_swatch_config?colorname=PA321")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        
        swatch = data["swatches"][0]
        assert swatch["colorname"] == "PA321"
        assert swatch["color_model"] == "PROCESS"
        assert swatch["color_space"] == "CMYK"
        assert swatch["colorvalues"] == "40,40,40,40"
    
    def test_get_swatches_with_invalid_colorname_returns_404(self, client):
        """Test that filtering by invalid colorname returns 404."""
        response = client.get("/get_swatch_config?colorname=NONEXISTENT")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Colorname 'NONEXISTENT' not found"
    
    def test_get_swatches_with_empty_colorname(self, client):
        """Test behavior when colorname parameter is empty."""
        response = client.get("/get_swatch_config?colorname=")
        # Empty colorname is treated as None, so returns all swatches
        assert response.status_code == 200
        data = response.json()
        assert len(data["swatches"]) == len(SWATCH_DATA)
    
    def test_get_swatches_case_sensitive_colorname(self, client):
        """Test that colorname filtering is case sensitive."""
        response = client.get("/get_swatch_config?colorname=dieline")
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
            assert "colorname" in swatch
            assert "color_model" in swatch
            assert "color_space" in swatch
            assert "colorvalues" in swatch
            
            # Validate types
            assert isinstance(swatch["colorname"], str)
            assert isinstance(swatch["color_model"], str)
            assert isinstance(swatch["color_space"], str)
            assert isinstance(swatch["colorvalues"], str)
            
            # Validate enum values
            assert swatch["color_model"] in ["SPOT", "PROCESS"]
            assert swatch["color_space"] in ["CMYK", "RGB", "LAB"]
    
    def test_multiple_query_parameters(self, client):
        """Test behavior with multiple query parameters (only colorname should be used)."""
        response = client.get("/get_swatch_config?colorname=DIELINE&other_param=value")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["swatches"]) == 1
        assert data["swatches"][0]["colorname"] == "DIELINE"
    
    def test_content_type_header(self, client):
        """Test that the endpoint returns correct content type."""
        response = client.get("/get_swatch_config")
        assert response.headers["content-type"] == "application/json"
    
    def test_all_expected_swatches_present(self, client):
        """Test that all expected swatches from SWATCH_DATA are returned."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        colornames = [swatch["colorname"] for swatch in data["swatches"]]
        expected_colornames = [swatch.colorname for swatch in SWATCH_DATA]
        
        assert set(colornames) == set(expected_colornames)
    
    def test_swatch_data_integrity(self, client):
        """Test that returned data matches the source data exactly."""
        response = client.get("/get_swatch_config")
        assert response.status_code == 200
        
        data = response.json()
        
        # Create a mapping of returned data by colorname for easy lookup
        returned_swatches = {swatch["colorname"]: swatch for swatch in data["swatches"]}
        
        # Compare each swatch in SWATCH_DATA with returned data
        for expected_swatch in SWATCH_DATA:
            returned_swatch = returned_swatches[expected_swatch.colorname]
            
            assert returned_swatch["colorname"] == expected_swatch.colorname
            assert returned_swatch["color_model"] == expected_swatch.color_model
            assert returned_swatch["color_space"] == expected_swatch.color_space
            assert returned_swatch["colorvalues"] == expected_swatch.colorvalues


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
            colorname="TEST_COLOR",
            color_model=ColorModel.SPOT,
            color_space=ColorSpace.RGB,
            colorvalues="255,0,0"
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
        """Test that colorvalues are in expected comma-separated format."""
        response = client.get("/get_swatch_config")
        data = response.json()
        
        for swatch in data["swatches"]:
            colorvalues = swatch["colorvalues"]
            # Should be comma-separated values
            assert isinstance(colorvalues, str)
            assert "," in colorvalues or colorvalues.isdigit()  # Single value or comma-separated
            
            # Split and check that all parts are numeric
            values = colorvalues.split(",")
            for value in values:
                assert value.strip().isdigit(), f"Invalid color value: {value}"


class TestParameterizedTests:
    """Parametrized tests using fixtures"""
    
    def test_valid_colornames(self, client, sample_colornames):
        """Test all valid colornames return correct results."""
        for colorname in sample_colornames:
            response = client.get(f"/get_swatch_config?colorname={colorname}")
            assert response.status_code == 200
            data = response.json()
            assert len(data["swatches"]) == 1
            assert data["swatches"][0]["colorname"] == colorname
    
    def test_invalid_colornames(self, client, invalid_colornames):
        """Test all invalid colornames return 404."""
        for colorname in invalid_colornames:
            response = client.get(f"/get_swatch_config?colorname={colorname}")
            if colorname == "":
                # Empty colorname returns all swatches
                assert response.status_code == 200
            else:
                assert response.status_code == 404
                assert "not found" in response.json()["detail"].lower()
