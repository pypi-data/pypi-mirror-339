# Copyright 2025 Cloutfit.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pytest
from unittest.mock import patch

from digitalocean_manager.client import DigitalOceanClient


@pytest.fixture
def mock_config():
    """Fixture to mock the Config class."""
    with patch("digitalocean_manager.client.Config") as MockConfig:
        mock_instance = MockConfig.return_value
        mock_instance.DIGITALOCEAN_TOKEN = "fake-token"
        mock_instance.json_indent = 2
        yield mock_instance


@pytest.fixture
def mock_pydo_client():
    """Fixture to mock the pydo.Client class."""
    with patch("digitalocean_manager.client.pydo.Client") as MockClient:
        yield MockClient


def test_digitalocean_client_initialization(mock_config, mock_pydo_client):
    """Test if the client initializes correctly."""
    client = DigitalOceanClient()
    
    # Ensure pydo.Client is instantiated with the correct token
    mock_pydo_client.assert_called_once_with(token="fake-token")

    # Ensure the config instance is assigned
    assert client.config is mock_config


def test_get_client(mock_config, mock_pydo_client):
    """Test if get_client() returns the expected client instance."""
    client = DigitalOceanClient()
    
    assert client.get_client() is mock_pydo_client.return_value


def test_raise_api_error(mock_config):
    """Test if raise_api_error() raises an exception with the expected message."""
    client = DigitalOceanClient()
    error_response = {"error": "Something went wrong"}

    with pytest.raises(Exception) as exc_info:
        client.raise_api_error(error_response)

    expected_message = "API Error\n" + json.dumps(error_response, indent=2)
    assert str(exc_info.value) == expected_message