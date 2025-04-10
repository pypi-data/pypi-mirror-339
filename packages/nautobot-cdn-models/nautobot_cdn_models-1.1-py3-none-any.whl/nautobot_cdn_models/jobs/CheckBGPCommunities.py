from nautobot.apps.jobs import Job, StringVar

import paramiko
import re
import requests
import os

def is_dev_environment():
    return os.environ.get('ENVIRONMENT', '').lower() == 'development'

if is_dev_environment():
    graphql_url = "http://nautobot1:8080/api/graphql/"
    graphql_headers = {
    'Authorization': os.environ.get('DEV_NAUTOBOT_API_TOKEN')
    }
    AKAMAI_HOST = os.environ.get('DEV_AKAMAI_HOST')
    AKAMAI_USER = os.environ.get('DEV_AKAMAI_USER')
    AKAMAI_PASS = os.environ.get('DEV_AKAMAI_PASS')
else:
    graphql_url = "https://localhost/api/graphql/"
    graphql_headers = {
    'Authorization': os.environ.get('NAUTOBOT_API_TOKEN'),
    }
    AKAMAI_HOST = os.environ.get('AKAMAI_HOST')
    AKAMAI_USER = os.environ.get('AKAMAI_USER')
    AKAMAI_PASS = os.environ.get('AKAMAI_PASS')


name = "Akamai CDN Tools"
class CheckBGPCommunities(Job):
    ip = StringVar(
        description="Enter an IP address (IPv4 or IPv6)",
        required=True,
    )

    class Meta:
        name = "Check Akamai BGP Communities"
        description = "This job checks BGP communities for a given IP address against akamais BGP feed."
        
    def run(self, ip):
        ip_address = ip

        # Hardcoded remote server details
        remote_host = AKAMAI_HOST
        ssh_user = AKAMAI_USER
        ssh_password = AKAMAI_PASS

        # Determine the vtysh command based on IP type
        if ":" in ip_address:  # IPv6
            command = f'vtysh -c "sh bgp {ip_address}"'
        else:  # IPv4
            command = f'vtysh -c "sh ip bgp {ip_address}"'

        # Connect to the remote server and execute the command
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_host, username=ssh_user, password=ssh_password)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            ssh.close()
        except Exception as e:
            self.logger.error(f"SSH connection or command execution failed: {e}")
            return

        # Parse the output to extract community information
        communities = set()
        match = re.findall(r"Community: (.+)", output)
        if match:
            for line in match:
                communities.update(line.split())

        if not communities:
            self.logger.warning("No communities found in the BGP output.")
            return

        self.logger.info(f"Extracted communities from BGP output: {communities}")
        self.logger.info(f"this is the url used {graphql_url}")

        # Query Nautobot GraphQL API
        query = """
        query {
          cdn_config_contexts {
            name
            data
            cdnsites {
              rel_cdnsite_devices {
                name
                id
                primary_ip4 {
                  address
                }
                primary_ip6 {
                  address
                }
              }
            }
          }
        }
        """
        payload = {}
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        
        try:
            if is_dev_environment():
                response = requests.post(f"{graphql_url}?query={query}", headers=graphql_headers, json=payload)
            else:
                response = requests.post(f"{graphql_url}?query={query}", headers=graphql_headers, json=payload, verify=False)
                
            if response.status_code != 200:
                self.logger.error(f"GraphQL query failed with status {response.status_code}: {response.text}")
                return

            # Validate the response structure
            response_json = response.json()
            if "data" not in response_json or "cdn_config_contexts" not in response_json["data"]:
                self.logger.error(f"GraphQL query returned an unexpected structure: {response_json}")
                return

            cdn_config_contexts = response_json["data"]["cdn_config_contexts"]
            if not cdn_config_contexts:
                self.logger.warning("GraphQL query executed successfully but returned no data.")
                return
        except Exception as e:
            self.logger.error(f"Failed to query Nautobot GraphQL API: {e}")
            return

        # Filter results and prepare output
        results = []
        for context in cdn_config_contexts:
            context_data = context.get("data", {})
            bgp_communities = context_data.get("bgp_communities", [])

            # Extract all mapclient values from bgp_communities
            mapclient_communities = set()
            for community in bgp_communities:
                mapclient = community.get("mapclient", "").strip()
                if mapclient:
                    mapclient_communities.add(mapclient)

            # Find if there is any overlap between vtysh communities and mapclient communities
            matching_communities = communities.intersection(mapclient_communities)

            if matching_communities:
                matching_community = str(next(iter(matching_communities), ""))
                for site in context.get("cdnsites", []):
                    for device in site.get("rel_cdnsite_devices", []):
                        device_name = device.get("name")
                        device_id = str(device.get("id", ""))
                        primary_ip4 = device.get("primary_ip4", {}).get("address", "N/A")
                        primary_ip6 = device.get("primary_ip6", {}).get("address", "N/A")
                        results.append({
                            "device": device_name,
                            "device_id": device_id,
                            "ipv4": primary_ip4,
                            "ipv6": primary_ip6,
                            "matching_bgp_community": matching_community,
                        })

                self.logger.success(f"Matching Community: {matching_community}")
                for result in results:
                    self.logger.info(f"Device Name: {result['device']}, "
                                  f"Primary IPv4: {result['ipv4']}, "
                                  f"Primary IPv6: {result['ipv6']}, "
                                  f"Device ID: {result['device_id']}, "
                                  f"BGP Community: {result['matching_bgp_community']}")
                break  # Stop processing further contexts if a match is found
        return {"results": results}
    