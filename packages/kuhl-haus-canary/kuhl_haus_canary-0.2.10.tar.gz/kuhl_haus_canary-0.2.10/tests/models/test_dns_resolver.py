import json
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock

from kuhl_haus.canary.models.dns_resolver import DnsResolver, DnsResolverList


# Using IP addresses from the 192.0.2.0/24 range (TEST-NET-1) which is reserved for
# documentation and examples as per RFC 5737. These addresses are guaranteed to not be
# routable on the public internet, making them ideal for unit testing.


def test_dns_resolver_creation():
    """Test that a DnsResolver object can be created with the expected attributes."""
    # Arrange
    name = "Test DNS"
    ip_address = "192.0.2.1"

    # Act
    sut = DnsResolver(name=name, ip_address=ip_address)

    # Assert
    assert sut.name == name
    assert sut.ip_address == ip_address


def test_dns_resolver_to_json():
    """Test that a DnsResolver can be serialized to JSON."""
    # Arrange
    sut = DnsResolver(name="Alpha DNS", ip_address="192.0.2.2")

    # Act
    result = sut.to_json()

    # Assert
    assert json.loads(result) == {"name": "Alpha DNS", "ip_address": "192.0.2.2"}


def test_dns_resolver_from_dict():
    """Test that a DnsResolver can be created from a dictionary."""
    # Arrange
    data = {"name": "Beta DNS", "ip_address": "192.0.2.3"}

    # Act
    sut = DnsResolver.from_dict(data)

    # Assert
    assert sut.name == "Beta DNS"
    assert sut.ip_address == "192.0.2.3"


def test_dns_resolver_list_creation():
    """Test that a DnsResolverList object can be created with the expected attributes."""
    # Arrange
    resolver1 = DnsResolver(name="Primary DNS", ip_address="192.0.2.4")
    resolver2 = DnsResolver(name="Secondary DNS", ip_address="192.0.2.5")

    # Act
    sut = DnsResolverList(resolvers=[resolver1, resolver2])

    # Assert
    assert len(sut.resolvers) == 2
    assert sut.resolvers[0].name == "Primary DNS"
    assert sut.resolvers[0].ip_address == "192.0.2.4"
    assert sut.resolvers[1].name == "Secondary DNS"
    assert sut.resolvers[1].ip_address == "192.0.2.5"


def test_dns_resolver_list_to_json():
    """Test that a DnsResolverList can be serialized to JSON."""
    # Arrange
    resolver1 = DnsResolver(name="First DNS", ip_address="192.0.2.6")
    resolver2 = DnsResolver(name="Second DNS", ip_address="192.0.2.7")
    sut = DnsResolverList(resolvers=[resolver1, resolver2])

    # Act
    result = sut.to_json()

    # Assert
    expected = {
        "resolvers": [
            {"name": "First DNS", "ip_address": "192.0.2.6"},
            {"name": "Second DNS", "ip_address": "192.0.2.7"}
        ]
    }
    assert json.loads(result) == expected


def test_dns_resolver_list_from_dict():
    """Test that a DnsResolverList can be created from a dictionary."""
    # Arrange
    data = {
        "resolvers": [
            {"name": "Main DNS", "ip_address": "192.0.2.8"},
            {"name": "Backup DNS", "ip_address": "192.0.2.9"}
        ]
    }

    # Act
    sut = DnsResolverList.from_dict(data)

    # Assert
    assert len(sut.resolvers) == 2
    assert sut.resolvers[0].name == "Main DNS"
    assert sut.resolvers[0].ip_address == "192.0.2.8"
    assert sut.resolvers[1].name == "Backup DNS"
    assert sut.resolvers[1].ip_address == "192.0.2.9"


@patch("builtins.open", new_callable=mock_open,
       read_data='{"resolvers": [{"name": "Example DNS", "ip_address": "192.0.2.10"}]}')
@patch("json.load")
def test_dns_resolver_list_from_file_success(mock_json_load, mock_file):
    """Test loading DNS resolvers from a file successfully."""
    # Arrange
    file_path = "resolvers.json"
    mock_json_load.return_value = {
        "resolvers": [
            {"name": "Example DNS", "ip_address": "192.0.2.10"}
        ]
    }

    # Act
    result = DnsResolverList.from_file(file_path)

    # Assert
    assert len(result) == 1
    assert result[0].name == "Example DNS"
    assert result[0].ip_address == "192.0.2.10"
    mock_file.assert_called_once_with(file_path, 'r')


@patch("builtins.open")
@patch("builtins.print")
def test_dns_resolver_list_from_file_not_found(mock_print, mock_file):
    """Test handling of file not found when loading DNS resolvers."""
    # Arrange
    file_path = "nonexistent.json"
    mock_file.side_effect = FileNotFoundError()

    # Act
    result = DnsResolverList.from_file(file_path)

    # Assert
    assert result == []
    mock_print.assert_called_once_with(f"File {file_path} not found.")


@patch("builtins.open", new_callable=mock_open, read_data='invalid json')
@patch("json.load")
@patch("builtins.print")
def test_dns_resolver_list_from_file_invalid_json(mock_print, mock_json_load, mock_file):
    """Test handling of invalid JSON when loading DNS resolvers."""
    # Arrange
    file_path = "invalid.json"
    mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

    # Act
    result = DnsResolverList.from_file(file_path)

    # Assert
    assert result == []
    mock_print.assert_called_once_with(f"Error decoding JSON from file {file_path}")


@patch("builtins.open", new_callable=mock_open,
       read_data='{"resolvers": [{"name": "Mock DNS", "ip_address": "192.0.2.11"}]}')
def test_dns_resolver_list_from_file_calls_from_dict(mock_file):
    """Test that from_file correctly calls from_dict method."""
    # Arrange
    file_path = "resolvers.json"

    # Act
    with patch.object(DnsResolverList, 'from_dict', return_value=DnsResolverList(
            resolvers=[DnsResolver(name="Mock DNS", ip_address="192.0.2.11")])) as mock_from_dict:
        result = DnsResolverList.from_file(file_path)

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], DnsResolver)
    mock_from_dict.assert_called_once()


def test_dns_resolver_list_empty():
    """Test that a DnsResolverList can be created with an empty list of resolvers."""
    # Arrange & Act
    sut = DnsResolverList(resolvers=[])

    # Assert
    assert len(sut.resolvers) == 0
    assert sut.resolvers == []


def test_dns_resolver_equality():
    """Test that two DnsResolver objects with the same attributes are equal."""
    # Arrange
    resolver1 = DnsResolver(name="Identical DNS", ip_address="192.0.2.12")
    resolver2 = DnsResolver(name="Identical DNS", ip_address="192.0.2.12")

    # Act & Assert
    assert resolver1 == resolver2


def test_dns_resolver_inequality():
    """Test that two DnsResolver objects with different attributes are not equal."""
    # Arrange
    resolver1 = DnsResolver(name="First DNS", ip_address="192.0.2.13")
    resolver2 = DnsResolver(name="Different DNS", ip_address="192.0.2.14")

    # Act & Assert
    assert resolver1 != resolver2
