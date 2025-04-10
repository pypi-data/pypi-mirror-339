from nautobot.apps.jobs import JobButtonReceiver
from nautobot.extras.models import Status
import requests
import os

# Akamai API configuration
beta_akamai_api_url = os.environ.get('BETA_AKAMAI_URL')
beta_akamai_api_token = os.environ.get('BETA_AKAMAI_API_TOKEN')
prod_akamai_api_url = os.environ.get('PROD_AKAMAI_URL')
prod_akamai_api_token = os.environ.get('PROD_AKAMAI_API_TOKEN')
ent_akamai_api_url = os.environ.get('ENT_AKAMAI_URL')
ent_akamai_api_token = os.environ.get('ENT_AKAMAI_API_TOKEN')

# Job Button to set status to Maintenance
class LcdnNodeToMaintenance(JobButtonReceiver):
    class Meta:
        name = "Set Node to Maintenance"
        description = "Set the Akamai Node status to Maintenance via the RestAPI"
        job_model = "dcim.device"

    def receive_job_button(self, obj):
        """Set the node status to Maintenance when the button is clicked."""
        device = obj
        user = self.user
        
        self.logger.info(f"Job invoked for device {device} by user {user}")
        
        if not device:
            self.logger.error("No device provided")
            return

        if "hpc" not in device.name.lower() and "mid" not in device.name.lower():
            self.logger.info(f"Skipping device {device.name}, name does not contain 'HPC' or 'MID'")
            return

        current_status = device.status.name if device.status else "Unknown"
        new_status = "Maintenance"
        
        self.logger.info(f"Current status: {current_status}, Attempting to set new status: {new_status}")

        try:
            node_info = self.get_akamai_node_info(device)
            if node_info is None:
                raise Exception("Failed to retrieve Akamai node information")

            response_status = self.update_akamai_node(device, new_status, node_info)
            if response_status != 200:
                raise Exception(f"Failed to update Akamai node, status code: {response_status}")

            new_status_obj = Status.objects.get(name=new_status)
            device.status = new_status_obj
            device.save()
                
            self.logger.success(f"Updated Akamai node {device.name} to status {new_status} by {user}")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            self.logger.error(f"Failed to update Akamai node {device.name}: {str(e)}")

    def get_akamai_node_info(self, device):
        if 'beta' in device.role.name.lower():
            amc_api_url = beta_akamai_api_url
            amc_api_token = beta_akamai_api_token
        else:
            amc_api_url = prod_akamai_api_url
            amc_api_token = prod_akamai_api_token
        headers = {
            'Authorization': f'Bearer {amc_api_token}',
            'Content-Type': 'application/json',
        }
        url = f'{amc_api_url}infrastructure/v1/nodes/{device.custom_field_data.get("akamai_node_id")}'  
        self.logger.info(f"URL for GET request: {url}")
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None

        if response.status_code == 200:
            node_info = response.json()
            if node_info['hostname'] != device.name:
                self.logger.error(f'Akamai site ID does not match for device {device.name}')
                return None
            return node_info
        elif response.status_code == 404:
            self.logger.error(f'Akamai node ID {device.custom_field_data.get("akamai_node_id")} does not exist on the AMC')
            return None
        else:
            self.logger.error(f'Failed to get Akamai node information. Status code: {response.status_code}')
            return None

    def update_akamai_node(self, device, status, node_info):
        if node_info is None:
            self.logger.error(f"Node info is None for device {device.name}")
            return None

        if 'beta' in device.role.name.lower():
            amc_api_url = beta_akamai_api_url
            amc_api_token = beta_akamai_api_token
        else:
            amc_api_url = prod_akamai_api_url
            amc_api_token = prod_akamai_api_token
            
        headers = {
            'Authorization': f'Bearer {amc_api_token}',
            'Content-Type': 'application/json',
        }
        
        data = node_info.copy() if node_info else {}
        data['administrativeState'] = status.upper()
        
        url = f'{amc_api_url}infrastructure/v1/nodes/{device.custom_field_data.get("akamai_node_id")}'  
        self.logger.info(f"URL for PUT request: {url}")

        response = requests.put(url, headers=headers, verify=False, json=data)
        return response.status_code

# Job Button to set status to Active
class LcdnNodeToActive(JobButtonReceiver):
    class Meta:
        name = "Set Node to Active"
        description = "Set the Akamai Node status to Active via the RestAPI"
        job_model = "dcim.device"

    def receive_job_button(self, obj):
        """Set the node status to Active when the button is clicked."""
        device = obj
        user = self.user
        
        self.logger.info(f"Job invoked for device {device} by user {user}")
        
        if not device:
            self.logger.error("No device provided")
            return

        if "hpc" not in device.name.lower() and "mid" not in device.name.lower():
            self.logger.info(f"Skipping device {device.name}, name does not contain 'HPC' or 'MID'")
            return

        current_status = device.status.name if device.status else "Unknown"
        new_status = "Active"
        
        self.logger.info(f"Current status: {current_status}, Attempting to set new status: {new_status}")

        try:
            node_info = self.get_akamai_node_info(device)
            if node_info is None:
                raise Exception("Failed to retrieve Akamai node information")

            response_status = self.update_akamai_node(device, new_status, node_info)
            if response_status != 200:
                raise Exception(f"Failed to update Akamai node, status code: {response_status}")

            new_status_obj = Status.objects.get(name=new_status)
            device.status = new_status_obj
            device.save()
                
            self.logger.success(f"Updated Akamai node {device.name} to status {new_status} by {user}")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            self.logger.error(f"Failed to update Akamai node {device.name}: {str(e)}")

    def get_akamai_node_info(self, device):
        if 'beta' in device.role.name.lower():
            amc_api_url = beta_akamai_api_url
            amc_api_token = beta_akamai_api_token
        else:
            amc_api_url = prod_akamai_api_url
            amc_api_token = prod_akamai_api_token
        headers = {
            'Authorization': f'Bearer {amc_api_token}',
            'Content-Type': 'application/json',
        }
        url = f'{amc_api_url}infrastructure/v1/nodes/{device.custom_field_data.get("akamai_node_id")}'  
        self.logger.info(f"URL for GET request: {url}")
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None

        if response.status_code == 200:
            node_info = response.json()
            if node_info['hostname'] != device.name:
                self.logger.error(f'Akamai site ID does not match for device {device.name}')
                return None
            return node_info
        elif response.status_code == 404:
            self.logger.error(f'Akamai node ID {device.custom_field_data.get("akamai_node_id")} does not exist on the AMC')
            return None
        else:
            self.logger.error(f'Failed to get Akamai node information. Status code: {response.status_code}')
            return None

    def update_akamai_node(self, device, status, node_info):
        if node_info is None:
            self.logger.error(f"Node info is None for device {device.name}")
            return None

        if 'beta' in device.role.name.lower():
            amc_api_url = beta_akamai_api_url
            amc_api_token = beta_akamai_api_token
        else:
            amc_api_url = prod_akamai_api_url
            amc_api_token = prod_akamai_api_token
            
        headers = {
            'Authorization': f'Bearer {amc_api_token}',
            'Content-Type': 'application/json',
        }
        
        data = node_info.copy() if node_info else {}
        data['administrativeState'] = status.upper()
        
        url = f'{amc_api_url}infrastructure/v1/nodes/{device.custom_field_data.get("akamai_node_id")}'  
        self.logger.info(f"URL for PUT request: {url}")

        response = requests.put(url, headers=headers, verify=False, json=data)
        return response.status_code