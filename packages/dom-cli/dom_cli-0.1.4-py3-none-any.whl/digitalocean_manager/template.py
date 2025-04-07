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

from digitalocean_manager.config import Config
from digitalocean_manager.project import ProjectPaths
from digitalocean_manager.reader import dict_from_file, read_file


config = Config()

def droplet_template(
    template_name: str,
    droplet_name: str,
    keys: tuple,
    volumes: tuple,
    tags: tuple,
    cloud_config_name: str,
) -> dict:
    """
    Create a droplet configuration dictionary based on a template.

    Args:
        template_name (str): Name of the droplet template.
        droplet_name (str): Name for the new droplet.
        keys (tuple): Tuple of SSH key IDs.
        volumes (tuple): Tuple of volume IDs.
        tags (tuple): Tuple of tags for the droplet.
        cloud_config_name (str): Name of the cloud config file.

    Returns:
        dict: Droplet configuration.
    """
    droplet = dict_from_file(ProjectPaths.DROPLETS_DIR, f'{template_name}.json')
    droplet['name'] = droplet_name
    droplet['region'] = config.digitalocean_region
    droplet['ssh_keys'] = merge_unique_items(droplet.get('ssh_keys', []), keys)
    droplet['volumes'] = merge_unique_items(droplet.get('volumes', []), volumes)
    droplet['tags'] = merge_unique_items(droplet.get('tags', []), tags)
    droplet['user_data'] = cloud_config_file(cloud_config_name) if cloud_config_name else ''
    return droplet


def volume_template(
    template_name: str,
    volume_name: str,
    tags: tuple,
) -> dict:
    """
    Create a volume configuration dictionary based on a template.

    Args:
        template_name (str): Name of the volume template.
        volume_name (str): Name for the new volume.
        tags (tuple): Tuple of tags for the volume.

    Returns:
        dict: Volume configuration.
    """
    volume = dict_from_file(ProjectPaths.VOLUMES_DIR, f'{template_name}.json')
    volume['name'] = volume_name
    volume['region'] = config.digitalocean_region
    volume['tags'] = merge_unique_items(volume.get('tags', []), tags)
    return volume


def merge_unique_items(existing_items: list, new_items: tuple) -> list:
    """Merge a list and a tuple while ensuring unique elements.

    This function takes an existing list and a tuple with new items,
    merges them while removing duplicates, and returns a new list
    with unique elements.

    Args:
        existing_items (list): The original list of items.
        new_items (tuple or None): New items to be added. If None, the original list is returned.

    Returns:
        list: A merged list containing unique elements from both inputs.
    """
    return list(set(existing_items + list(new_items) if new_items else existing_items))


def cloud_config_file(name: str) -> str:
    """
    Read a cloud config YAML file.

    Args:
        name (str): Name of the cloud config file.

    Returns:
        str: Contents of the cloud config file.
    """
    return read_file(ProjectPaths.CLOUD_CONFIGS_DIR, f"{name}.yaml")


def raw_json_templates(basedir: str) -> list:
    """
    Load all JSON templates from a directory.

    Args:
        basedir (str): Path to the directory containing JSON templates.

    Returns:
        list: List of dictionaries representing templates.
    """
    templates = []
    for filename in [f for f in os.listdir(basedir) if f.endswith('.json')]:
        name, _ = os.path.splitext(filename)
        content = dict_from_file(basedir, filename)
        templates.append({name: content})
    return templates


def raw_droplet_templates() -> list:
    """
    Load all droplet templates as dictionaries.

    Returns:
        list: List of dictionaries representing droplet templates.
    """
    return raw_json_templates(ProjectPaths.DROPLETS_DIR)


def raw_volume_templates() -> list:
    """
    Load all volume templates as dictionaries.

    Returns:
        list: List of dictionaries representing volume templates.
    """
    return raw_json_templates(ProjectPaths.VOLUMES_DIR)