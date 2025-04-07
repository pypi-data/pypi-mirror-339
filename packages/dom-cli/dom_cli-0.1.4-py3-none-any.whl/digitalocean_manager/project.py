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
import json
import yaml
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectPaths:
    """
    Directory names and main config filename for the project.

    This class stores the directory paths and the main configuration file path
    used in the project. It uses `frozen=True` to make the instance immutable.

    Attributes:
        CLOUD_CONFIGS_DIR (str): The directory name for cloud configurations.
        DROPLETS_DIR (str): The directory name for droplets configurations.
        VOLUMES_DIR (str): The directory name for volumes configurations.
        CONFIG_FILENAME (str): The filename for the main project configuration file.
    """
    CLOUD_CONFIGS_DIR: str = "cloud-configs"
    DROPLETS_DIR: str = "droplets"
    VOLUMES_DIR: str = "volumes"
    CONFIG_FILENAME: str = "config.yaml"


class Project:
    """
    A class to handle the creation of a DigitalOcean Manager project structure.

    Attributes:
        PROJECT_DIR_STRUCTURE (dict): A predefined structure for directories and files.
        CONFIG_FILE (dict): Configuration for the project, including settings for regions, protected resources, etc.
    """

    # Initial dir structure with some example files.
    PROJECT_DIR_STRUCTURE = {
        ProjectPaths.CLOUD_CONFIGS_DIR: [
            {
                'filename': 'base.yaml',
                'content': {
                    'package_update': True,
                    'packages': [
                        'curl',
                        'git',
                        'htop',
                        'python3',
                        'python3-pip',
                        'python3-venv',
                        'tree',
                        'wget',
                    ],
                },
            },
        ],
        ProjectPaths.DROPLETS_DIR: [
            {
                'filename': 'cpu-mini.json',
                'content': {
                    'name': None,  # dinamically set
                    'region': None, # dinamically set
                    'size': 's-1vcpu-1gb',
                    'image': 'ubuntu-22-04-x64',
                    'ssh_keys': [],
                    'backups': False,
                    'ipv6': False,
                    'monitoring': False,
                    'tags': [],
                    'user_data': None, # dinamically set
                    'volumes': [],
                },
            },
            {
                'filename': 'nvidia-h100.json',
                'content': {
                    'name': None,  # dinamically set
                    'region': None, # dinamically set
                    'size': 'gpu-h100x1-80gb',
                    'image': 'gpu-h100x1-base',
                    'ssh_keys': [],
                    'backups': False,
                    'ipv6': False,
                    'monitoring': False,
                    'tags': [],
                    'user_data': None, # dinamically set
                },
            },
        ],
        ProjectPaths.VOLUMES_DIR: [
            {
                'filename': 'models.json',
                'content': {
                    "name": None,  # dinamically set
                    "size_gigabytes": 100,
                    "description": "Models volume",
                    "region": None, # dinamically set
                    "filesystem_type": "ext4",
                    "filesystem_label": "models",
                },
            },
        ],
    }

    # Main config file
    CONFIG_FILE = {
        'digitalocean_region': {
            'help': '# DigitalOcean datacenter region slug (str).\n# Full detail here: https://docs.digitalocean.com/platform/regional-availability/',
            'value': 'nyc2',
        },
        'protected_droplets': {
            'help': '# List of (int) protected droplets IDs.\n# You can\'t stop/delete a protected droplet.\n# You can\'t detach a volume from a protected droplet.',
            'value': [],
        },
        'protected_volumes': {
            'help': '# List of (str) protected volumes IDs.\n# You can\'t delete a protected volume.',
            'value': []
        },
        'json_indent': {
            'help': '# JSON indentation level (int) for raw outputs.',
            'value': 4,
        },
        'ping_interval': {
            'help': '# Action ping interval (float) in seconds.',
            'value': 1,
        },
    }

    def __init__(self):
        pass
    
    def create(self) -> None:
        """
        Create the DigitalOcean Manager configuration structure.

        This method creates the necessary directories and files for the DigitalOcean Manager project.
        It will use the predefined structure in `PROJECT_DIR_STRUCTURE` and the configuration settings
        in `CONFIG_FILE`.

        Raises:
            Exception: If there is an error creating any directories or files.
        """
        self._create_config_file()
        for dirname, files in Project.PROJECT_DIR_STRUCTURE.items():
            if dirname != '.':
                self._create_dir(dirname)
            for file in files:
                filename = file['filename']
                # Json files
                if filename.endswith('json'):
                    content = json.dumps(file['content'], indent=4) + '\n'
                # Yaml files
                elif filename.endswith('yaml'):
                    content = yaml.dump(
                        file['content'],
                        default_flow_style=False,
                        sort_keys=False,
                        Dumper=Dumper,
                    )
                    if 'cloud-config' in dirname:
                        content = '#cloud-config\n' + content
                # Unknown files
                else:
                    raise Exception("Error: file extension is not supported.")
                self._create_file(filename, content, dirname)
    
    def _create_dir(self, dirname: str) -> None:
        """
        Create a directory.

        Args:
            dirname (str): The name of the directory to create.

        Raises:
            Exception: If there is an error creating the directory.
        """
        try:
            os.mkdir(os.path.join(os.getcwd(), dirname))
        except Exception as e:
            print(f"Error creating directory {dirname}: {e}")

    def _create_file(self, filename: str, content: str, dest: str) -> None:
        """
        Create a file in the specified directory.

        Args:
            filename (str): The name of the file to create.
            content (str): The content to write to the file.
            dest (str): The destination directory where the file should be created.

        Raises:
            Exception: If there is an error creating the file.
        """
        try:
            with open(os.path.join(os.getcwd(), dest, filename), 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error creating file {dest}/{filename}: {e}")
    
    def _create_config_file(self) -> None:
        """
        Create the main config file.

        This method creates the configuration file defined in `CONFIG_FILE` and writes its content
        in YAML format to the specified file path.

        Raises:
            FileExistsError: If the config file already exists.
            Exception: If there is an error creating the config file.
        """
        try:
            if os.path.exists(ProjectPaths.CONFIG_FILENAME):
                raise FileExistsError(f"'{ProjectPaths.CONFIG_FILENAME}' already exists.")
            with open(ProjectPaths.CONFIG_FILENAME, 'w') as config_file:
                newline = ''
                for key, item in Project.CONFIG_FILE.items():
                    config_file.write(f"{newline}{item['help']}\n")
                    yaml.dump(
                        {key: item['value']},
                        config_file,
                        default_flow_style=False,
                        allow_unicode=True,
                        Dumper=Dumper,
                    )
                    newline = '\n'
        except Exception as e:
            print(f"Error creating the main config file: {e}")


# Workaround for yaml better output format
# https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)