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

import os
import pytest
import sys
from unittest.mock import patch


MODULE_NAME = "digitalocean_manager.config"


@pytest.fixture(autouse=True)
def reset_config_instance():
    """Fixture to reset the Config instance."""
    # Check if the module is already loaded and remove it from sys.modules
    if MODULE_NAME in sys.modules:
        print('[removing config module]', end=' ')
        del sys.modules[MODULE_NAME]

    yield


@pytest.fixture
def mock_dict_from_file():
    """Fixture to mock the dict_from_file function."""
    with patch("digitalocean_manager.config.dict_from_file") as mock_func:
        mock_func.return_value = {"json_indent": 2}
        yield mock_func


@pytest.fixture
def mock_env():
    """Fixture to mock environment variables."""
    with patch.dict(os.environ, {"DIGITALOCEAN_TOKEN": "env-token"}):
        yield


@pytest.fixture
def mock_project_paths():
    """Fixture to mock ProjectPaths.CONFIG_FILENAME."""
    with patch("digitalocean_manager.config.ProjectPaths.CONFIG_FILENAME", "config.json"):
        yield


def test_config_singleton(mock_dict_from_file, mock_project_paths):
    """Test that Config follows the singleton pattern."""
    from digitalocean_manager.config import Config

    config1 = Config()
    config2 = Config()
    
    assert config1 is config2  # Singleton instance


def test_config_reads_from_env(mock_dict_from_file, mock_env, mock_project_paths):
    """Test that Config retrieves environment variables correctly."""
    from digitalocean_manager.config import Config

    config = Config()
    
    assert config.DIGITALOCEAN_TOKEN == "env-token"  # Env variable should take priority


def test_config_reads_from_file(mock_dict_from_file, mock_env, mock_project_paths):
    """Test that Config retrieves values from the config file."""
    from digitalocean_manager.config import Config

    config = Config()
    
    assert config.json_indent == 2  # Value from dict_from_file


def test_config_missing_env_variable(mock_dict_from_file, mock_project_paths):
    """Test that accessing a missing environment variable raises ValueError."""
    from digitalocean_manager.config import Config

    config = Config()

    with pytest.raises(ValueError) as exc_info:
        _ = config.MISSING_ENV_VAR

    assert "Environment variable 'MISSING_ENV_VAR' is not set." in str(exc_info.value)


def test_config_missing_config_attribute(mock_dict_from_file, mock_project_paths):
    """Test that accessing a missing config file attribute raises ValueError (not AttributeError)."""
    from digitalocean_manager.config import Config

    config = Config()
    
    with pytest.raises(ValueError) as exc_info:
        _ = config.MISSING_CONFIG_KEY

    assert "Environment variable 'MISSING_CONFIG_KEY' is not set." in str(exc_info.value)