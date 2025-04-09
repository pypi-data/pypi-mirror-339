import pytest
import json
import tempfile
import os
from urllib.parse import urlparse
from unittest.mock import patch, mock_open

from kuhl_haus.canary.models.endpoint_model import EndpointModel


@pytest.fixture
def basic_endpoint_model():
    return EndpointModel(mnemonic="test", hostname="example.com")


@pytest.fixture
def complete_endpoint_model():
    return EndpointModel(
        mnemonic="complete",
        hostname="example.org",
        scheme="http",
        port=8080,
        path="/api/v1",
        query=[("key1", "value1"), ("key2", "value2")],
        fragment="section1",
        healthy_status_code=201,
        json_response=True,
        status_key="state",
        healthy_status="OPERATIONAL",
        version_key="version_info",
        connect_timeout=10.0,
        read_timeout=15.0,
        ignore=True
    )


def test_endpoint_model_initialization_with_required_fields():
    """Test that EndpointModel can be initialized with only required fields."""
    # Arrange & Act
    sut = EndpointModel(mnemonic="test", hostname="example.com")

    # Assert
    assert sut.mnemonic == "test"
    assert sut.hostname == "example.com"
    assert sut.scheme == "https"  # Default value
    assert sut.port == 443  # Default value
    assert sut.path == "/"  # Default value


def test_endpoint_model_initialization_with_all_fields(complete_endpoint_model):
    """Test that EndpointModel can be initialized with all fields."""
    # Assert
    sut = complete_endpoint_model
    assert sut.mnemonic == "complete"
    assert sut.hostname == "example.org"
    assert sut.scheme == "http"
    assert sut.port == 8080
    assert sut.path == "/api/v1"
    assert sut.query == [("key1", "value1"), ("key2", "value2")]
    assert sut.fragment == "section1"
    assert sut.healthy_status_code == 201
    assert sut.json_response is True
    assert sut.status_key == "state"
    assert sut.healthy_status == "OPERATIONAL"
    assert sut.version_key == "version_info"
    assert sut.connect_timeout == 10.0
    assert sut.read_timeout == 15.0
    assert sut.ignore is True


def test_endpoint_model_url_property_basic(basic_endpoint_model):
    """Test the url property with basic settings."""
    # Arrange
    sut = basic_endpoint_model

    # Act
    result = sut.url

    # Assert
    parsed_url = urlparse(result)
    assert parsed_url.hostname == "example.com"
    assert parsed_url.scheme == "https"
    assert parsed_url.port == 443


def test_endpoint_model_url_property_with_path_and_port(basic_endpoint_model):
    """Test the url property with custom path and port."""
    # Arrange
    sut = basic_endpoint_model
    sut.path = "/api/health"
    sut.port = 8443

    # Act
    result = sut.url

    # Assert
    parsed_url = urlparse(result)
    assert parsed_url.hostname == "example.com"
    assert parsed_url.scheme == "https"
    assert parsed_url.port == 8443
    assert parsed_url.path == "/api/health"


def test_endpoint_model_url_property_with_query_params():
    """Test the url property with query parameters."""
    # Arrange
    sut = EndpointModel(
        mnemonic="test",
        hostname="example.com",
        query=[("param1", "value1"), ("param2", "value2")]
    )

    # Act
    result = sut.url

    # Assert
    parsed_url = urlparse(result)
    assert parsed_url.hostname == "example.com"
    assert parsed_url.query == 'param1=value1&param2=value2'


def test_endpoint_model_url_property_with_fragment():
    """Test the url property with a fragment."""
    # Arrange
    sut = EndpointModel(
        mnemonic="test",
        hostname="example.com",
        fragment="section"
    )

    # Act
    result = sut.url

    # Assert
    parsed_url = urlparse(result)
    assert parsed_url.hostname == "example.com"
    assert parsed_url.fragment == "section"


def test_endpoint_model_url_property_with_all_components(complete_endpoint_model):
    """Test the url property with all components (scheme, hostname, port, path, query, fragment)."""
    # Arrange
    sut = complete_endpoint_model

    # Act
    result = sut.url

    # Assert
    parsed_url = urlparse(result)
    assert parsed_url.hostname == "example.org"
    assert parsed_url.fragment == "section1"
    assert parsed_url.query == 'key1=value1&key2=value2'


def test_endpoint_model_normalize_path_empty():
    """Test __normalize_path with empty path."""
    # Arrange
    sut = EndpointModel(mnemonic="test", hostname="example.com")

    # Act
    result = sut._EndpointModel__normalize_path("")

    # Assert
    assert result == "/"


def test_endpoint_model_normalize_path_missing_leading_slash():
    """Test __normalize_path with path missing leading slash."""
    # Arrange
    sut = EndpointModel(mnemonic="test", hostname="example.com")

    # Act
    result = sut._EndpointModel__normalize_path("api/v1")

    # Assert
    assert result == "/api/v1"


def test_endpoint_model_normalize_path_duplicate_slashes():
    """Test __normalize_path with duplicate slashes."""
    # Arrange
    sut = EndpointModel(mnemonic="test", hostname="example.com")

    # Act
    result = sut._EndpointModel__normalize_path("//api//v1///endpoint//")

    # Assert
    assert result == "/api/v1/endpoint/"


@patch('builtins.open', new_callable=mock_open,
       read_data='[{"mnemonic": "test1", "hostname": "example.com"}, {"mnemonic": "test2", "hostname": "example.org"}]')
def test_from_file_success(mock_file):
    """Test from_file method with valid JSON file."""
    # Arrange & Act
    result = EndpointModel.from_file("dummy_path.json")

    # Assert
    assert len(result) == 2
    assert result[0].mnemonic == "test1"
    assert result[0].hostname == "example.com"
    assert result[1].mnemonic == "test2"
    assert result[1].hostname == "example.org"
    mock_file.assert_called_once_with("dummy_path.json", "r")


def test_from_file_with_real_file():
    """Test from_file method with a real temporary file."""
    # Arrange
    test_data = [
        {"mnemonic": "test1", "hostname": "example.com"},
        {"mnemonic": "test2", "hostname": "example.org", "port": 8080}
    ]

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(test_data, temp_file)
        temp_file_path = temp_file.name

    try:
        # Act
        result = EndpointModel.from_file(temp_file_path)

        # Assert
        assert len(result) == 2
        assert result[0].mnemonic == "test1"
        assert result[0].hostname == "example.com"
        assert result[1].mnemonic == "test2"
        assert result[1].hostname == "example.org"
        assert result[1].port == 8080
    finally:
        # Cleanup
        os.unlink(temp_file_path)


@patch('builtins.open', side_effect=FileNotFoundError())
def test_from_file_file_not_found(mock_file):
    """Test from_file method when file is not found."""
    # Arrange & Act
    with patch('builtins.print') as mock_print:
        result = EndpointModel.from_file("nonexistent_file.json")

    # Assert
    assert result == []
    mock_print.assert_called_once_with("File nonexistent_file.json not found.")


@patch('builtins.open', new_callable=mock_open, read_data='invalid json')
def test_from_file_invalid_json(mock_file):
    """Test from_file method with invalid JSON."""
    # Arrange & Act
    with patch('builtins.print') as mock_print:
        result = EndpointModel.from_file("invalid_json.json")

    # Assert
    assert result == []
    mock_print.assert_called_once_with("Error decoding JSON from file invalid_json.json")


def test_from_file_invalid_endpoint_model_data():
    """Test from_file method with JSON that doesn't match EndpointModel fields."""
    # Arrange
    test_data = [{"invalid_field": "value"}]  # Missing required fields

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(test_data, temp_file)
        temp_file_path = temp_file.name

    try:
        # Act & Assert
        with pytest.raises(TypeError):
            EndpointModel.from_file(temp_file_path)
    finally:
        # Cleanup
        os.unlink(temp_file_path)


def test_lru_cache_functionality_for_normalize_path():
    """Test that __normalize_path uses lru_cache effectively."""
    # Arrange
    sut = EndpointModel(mnemonic="test", hostname="example.com")

    # Act
    # Call the same path twice
    result1 = sut._EndpointModel__normalize_path("//api//test//")
    result2 = sut._EndpointModel__normalize_path("//api//test//")

    # Assert
    assert result1 == "/api/test/"
    assert result2 == "/api/test/"
    # We can't easily assert the cache was used, but at least we can verify same results
