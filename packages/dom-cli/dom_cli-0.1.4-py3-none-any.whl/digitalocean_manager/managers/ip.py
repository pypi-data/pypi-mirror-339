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

from digitalocean_manager.config import Config
from digitalocean_manager.client import DigitalOceanClient
from digitalocean_manager.managers.action import ActionManager


class IPManager:
    """
    Manages DigitalOcean Reserved IPs.

    Attributes:
        config (Config): Configuration object to handle settings and configurations.
        client (Client): DigitalOcean API client instance.
        action_manager (ActionManager): ActionManager instance to handle actions like assign.
    """

    def __init__(self):
        """
        Initializes the IPManager with the necessary configurations and client connections.
        """
        self.config = Config()
        self.client = DigitalOceanClient().get_client()
        self.action_manager = ActionManager()

    def list(self):
        """
        List all reserved IPs.

        This method retrieves and displays all reserved IPs associated with the account.

        Raises:
            Exception: If there is an error retrieving the list of reserved IPs.

        This method fetches all reserved IPs and prints their information.
        If any error occurs, it raises an exception.
        """
        try:
            resp = self.client.reserved_ips.list()
            if 'reserved_ips' in resp:
                for ip in resp['reserved_ips']:
                    if ip['region']['slug'] == self.config.digitalocean_region:
                        self.display(ip)
            else:
                self.client.raise_api_error(resp)
        except Exception as e:
            print(f"Error listing reserved IPs: {e}")

    def assign(self, reserved_ip: str, droplet_id: int) -> None:
        """
        Assign a reserved IP to a droplet.

        Args:
            reserved_ip (str): The reserved IP address to assign.
            droplet_id (int): The ID of the droplet to assign the IP to.

        Raises:
            Exception: If there is an error assigning the reserved IP to the droplet.

        This method assigns a reserved IP to a droplet and prints the response.
        If any error occurs, it raises an exception.
        """
        try:
            req = {
                "type": "assign",
                "droplet_id": droplet_id,
            }
            resp = self.client.reserved_ips_actions.post(reserved_ip=reserved_ip, body=req)
            if 'action' in resp:
                action = resp['action']
                self.action_manager.display(action)
                self.action_manager.ping(action['id'])
            else:
                self.client.raise_api_error(resp)
        except Exception as e:
            print(f"Error assigning IP: {e}")

    def unassign(self, reserved_ip: str) -> None:
        """
        Unassign a reserved IP from a droplet.

        Args:
            reserved_ip (str): The reserved IP address to unassign.

        Raises:
            Exception: If there is an error unassigning the reserved IP.
        """
        try:
            req = {"type": "unassign"}
            resp = self.client.reserved_ips_actions.post(reserved_ip=reserved_ip, body=req)
            if 'action' in resp:
                action = resp['action']
                self.action_manager.display(action)
                self.action_manager.ping(action['id'])
            else:
                self.client.raise_api_error(resp)
        except Exception as e:
            print(f"Error unassigning IP: {e}")

    def display(self, ip: dict) -> None:
        """
        Display information about a reserved IP.

        Args:
            ip (dict): The reserved IP object containing details about the IP.

        This method prints key information about the reserved IP, including its IP address,
        and droplet ID.
        """
        print(
            f"IP: {ip['ip']}, "
            f"Region: {ip['region']['slug']}, "
            f"Droplet ID: {ip['droplet']['id'] if ip['droplet'] else 'None'}"
        )