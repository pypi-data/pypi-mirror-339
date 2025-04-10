import re
import requests
import os

import logging
from django.contrib.auth import get_user_model
from types import SimpleNamespace

from nautobot.apps.jobs import JobButtonReceiver
from nautobot_cdn_models.models import CdnSite

from graphene_django.settings import graphene_settings
from graphql import get_default_backend
from graphql.error import GraphQLSyntaxError


LOGGER = logging.getLogger(__name__)

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

beta_akamai_api_url = os.environ.get('BETA_AKAMAI_URL')
beta_akamai_api_token = os.environ.get('BETA_AKAMAI_API_TOKEN')

prod_akamai_api_url = os.environ.get('PROD_AKAMAI_URL')
prod_akamai_api_token = os.environ.get('PROD_AKAMAI_API_TOKEN')

ent_akamai_api_url = os.environ.get('ENT_AKAMAI_URL')
ent_akamai_api_token = os.environ.get('ENT_AKAMAI_API_TOKEN')

dev_akamai_api_url = os.environ.get('DEV_AKAMAI_URL')
dev_akamai_api_token = os.environ.get('DEV_AKAMAI_API_TOKEN')


name = "Akamai CDN Tools"
class DeployAkamaiSite(JobButtonReceiver):
    class Meta:
        name = "Deploy or Update an Akamai Site"
        description = "Deploy or update an Akamai site using Nautobot data and the LCDN API."
        
    def receive_job_button(self, obj):
        graphql_query = """
            query($cdnsite_id: ID!) {
                cdn_site(id: $cdnsite_id) {
                    id
                    name
                    location {
                        name
                        id
                    }
                    cdn_site_role {
                        name
                        id
                    }
                    cacheMemoryProfileId{
                        name
                        cacheMemoryProfileId
                    }
                    abbreviatedName
                    enableDisklessMode
                    neighbor1 {
                        name
                        siteId
                    }
                    neighbor1_preference
                    neighbor2 {
                        name
                        siteId
                    }
                    neighbor2_preference
                    bandwidthLimitMbps
                }
            }
        """
        cdn_site_role_name = None
        if obj.cdn_site_role:
            cdn_site_role_name = obj.cdn_site_role.name
            self.logger.info(f"cdn_site_role_name passed to create_akamai_site: {cdn_site_role_name}")
        else:
            self.logger.error(f"CDN Site '{obj.name}' is missing a cdn_site_role. This is a data error.")
            raise ValueError(f"CDN Site '{obj.name}' must have a cdn_site_role.")
        
        if hasattr(obj, 'cdn_site_role') and obj.cdn_site_role is not None and hasattr(obj.cdn_site_role, 'name'):
            cdn_site_role_name = obj.cdn_site_role.name
        else:
            # Handle the case where attributes are missing or None
            self.logger.error(f"CDN Site '{obj.name}' has an issue with cdn_site_role.")
            raise ValueError(f"CDN Site '{obj.name}' cdn_site_role or its name attribute is missing.")
        
        nb_data = self.graph_ql_query(
            request=self.request,
            obj=obj,
            query=graphql_query
        )
        create_site_payload = self.create_akamai_site(nb_data)
        
        bearer_token = None

        if cdn_site_role_name == "Beta_Site" or cdn_site_role_name == "Beta_Linear_Edge" or cdn_site_role_name == "Beta Linear Edge":
            base_url = beta_akamai_api_url
            bearer_token = beta_akamai_api_token
        elif cdn_site_role_name == "Market Linear Edge" or cdn_site_role_name == "Regional Internal Edge" or cdn_site_role_name == "Regional Linear Edge" or cdn_site_role_name == "Regional Linear MidTier" or cdn_site_role_name == "Regional VOD" or cdn_site_role_name == "Market VOD":
            base_url = prod_akamai_api_url
            bearer_token = prod_akamai_api_token
        elif cdn_site_role_name == "Spectrum Enterprise HPCs":
            base_url = ent_akamai_api_url
            bearer_token = ent_akamai_api_token
        elif cdn_site_role_name == "Dev_Site":
            base_url = dev_akamai_api_url
            bearer_token = dev_akamai_api_token
        else:
            # Log or handle the unknown role, but don't raise here yet
            self.logger.error(f"Unknown CDN site role encountered: {cdn_site_role_name}")
            # If no token was set, raise an error here
            if bearer_token is None:
                raise ValueError(f"Bearer token not found for the given role: {cdn_site_role_name}")

        # Now bearer_token is either set or you've raised an error if it wasn't
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer_token}",
        }
        
        # Get neighbor site IDs
        neighbor1_siteid, neighbor2_siteid = self.get_site_id(nb_data, cdn_site_role_name)
        
        # Check if site exists, adjusting for 'beta_' prefix
        site_found, site_id = self.site_exists(nb_data, cdn_site_role_name)
        
        sites_url = f"{base_url}infrastructure/v1/sites"
        if not site_found:
            action = "create"
            # Creates the Site 
            response = requests.post(sites_url, json=create_site_payload, headers=headers, verify=False)
            if response.status_code == 201:
                # Parse response to get the akamai_site_id
                response_data = response.json()
                api_site_id = response_data.get("siteId")
                # Update the Nautobot Database with the new SiteId
                self.update_siteid_with_akamai_siteid(obj.name, api_site_id)
                self.logger.success(f"Site and services for '{obj.name}' {action}d successfully: {response.text}")
                # Adding services to site that was just created
                site_services_payload = self.update_akamai_site(nb_data, api_site_id, neighbor1_siteid, neighbor2_siteid, cdn_site_role_name)
                service_url = f"{base_url}lcdn-services/v1/sites/{api_site_id}"
                site_services_response = requests.put(service_url, json=site_services_payload, headers=headers, verify=False)
                if site_services_response.status_code == 200:
                    self.logger.success(f"Site and services for '{obj.name}' {action}d successfully: {site_services_response.text}")
                else:
                    self.logger.error(f"Failed to {action} site '{obj.name}': {site_services_response.text}, Status Code: {site_services_response.status_code}, Payload Code: {site_services_payload}")
            else:
                self.logger.error(f"Failed to {action} site '{obj.name}': {response.text}, Status Code: {response.status_code}, Payload Code: {response_data}")
        else:
            action = "update"
            # Updating services and bandwidth
            site_services_payload = self.update_akamai_site(nb_data, site_id, neighbor1_siteid, neighbor2_siteid, cdn_site_role_name)
            service_url = f"{base_url}lcdn-services/v1/sites/{site_id}"
            site_services_response = requests.put(service_url, json=site_services_payload, headers=headers, verify=False)
            if site_services_response.status_code == 200:
                self.logger.success(f"Site and services for '{obj.name}' {action}d successfully: {site_services_response.text}")
            else:
                self.logger.error(f"Failed to {action} site '{obj.name}': {site_services_response.text}, Status Code: {site_services_response.status_code}, Payload Code: {site_services_payload}")
        
        
        
        
    def graph_ql_query(self, request, obj, query):
        """Run GraphQL query and return only results (data)."""

        backend = get_default_backend()
        schema = graphene_settings.SCHEMA

        # GraphQL Variables
        variables = {"cdnsite_id": str(obj.pk)}

        # User context
        User = get_user_model()
        active_user = request.user if (hasattr(request, 'user') and request.user.is_authenticated) else User.objects.get(username='admin')
        context = SimpleNamespace(user=active_user)

        try:
            document = backend.document_from_string(schema, query)
        except GraphQLSyntaxError as error:
            return {"error": f"GraphQL Syntax Error: {str(error)}"}

        result = document.execute(context_value=context, variable_values=variables)

        if result.invalid or result.errors:
            return {"error": "GraphQL query failed", "details": result.errors}

        return result.data


    ### Creates the JSON blob for a new Site 
    def create_akamai_site(self, nb):
        # Create or update the site
        site_name = nb["cdn_site"]["name"]
        if site_name.startswith('beta_'):
            site_name = site_name[5:]  # Remove 'beta_' prefix
        
            create_site_payload = {
                "name": site_name,
                "abbreviatedName": f"{nb['cdn_site']['abbreviatedName']}",
            }
        return create_site_payload


    ### Creates the LCDN Services JSON blob for a Site after it has been created or already exists
    def update_akamai_site(self, nb, api_site_id, neighbor1_siteid, neighbor2_siteid, cdn_site_role_name ):
        # JSON Blob
        if "beta" in str(cdn_site_role_name).lower():
            site_services_payload = {
                "neighbors": [
                    {
                        "siteId": 9,
                        "preference": 600
                    },
                    {
                        "siteId": 11,
                        "preference": 500
                    }
                ],
                "enableDisklessMode": nb["cdn_site"]['enableDisklessMode'],
                "cacheMemoryProfileId": nb["cdn_site"]['cacheMemoryProfileId']['cacheMemoryProfileId'],
                "bandwidthLimitMbps": nb["cdn_site"]['bandwidthLimitMbps'],
                "siteId": api_site_id
                }
        if "linear" in str(cdn_site_role_name).lower() and (nb["cdn_site"]["neighbor1"] == "Carolinas_NCEast_NC_linear_shield" or nb["cdn_site"]["neighbor1"] == "NorthWest_NCWest_CO_linear_shield" or nb["cdn_site"]["neighbor1"] == "Carolinas_NCEast_NC_vod_shield" or nb["cdn_site"]["neighbor1"] == "NorthWest_NCWest_CO_vod_shield"):
            site_services_payload = {
                "neighbors": [
                    {
                        "siteId": neighbor1_siteid,
                        "preference": 600
                    },
                    {
                        "siteId": neighbor2_siteid,
                        "preference": 500
                    }
                ],
                "enableDisklessMode": nb["cdn_site"]['enableDisklessMode'],
                "cacheMemoryProfileId": nb["cdn_site"]['cacheMemoryProfileId']['cacheMemoryProfileId'],
                "siteId": api_site_id
                }
        elif "dev" in str(cdn_site_role_name).lower():
            site_services_payload = {
                "neighbors": [
                    {
                        "siteId": neighbor1_siteid,
                        "preference": 1000
                    },
                    {
                        "siteId": neighbor2_siteid,
                        "preference": 750
                    }
                ],
                "enableDisklessMode": nb["cdn_site"]['enableDisklessMode'],
                "cacheMemoryProfileId": nb["cdn_site"]['cacheMemoryProfileId']['cacheMemoryProfileId'],
                "bandwidthLimitMbps": nb["cdn_site"]['bandwidthLimitMbps'],
                "siteId": api_site_id
                }
        return site_services_payload

    ### Pulls the SiteId for existing sites that will be used as site neighbors
    def get_site_id(self, nb, cdn_site_role_name):
        bearer_token = None

        if cdn_site_role_name == "Beta_Site" or cdn_site_role_name == "Beta_Linear_Edge" or cdn_site_role_name == "Beta Linear Edge":
            base_url = beta_akamai_api_url
            bearer_token = beta_akamai_api_token
        elif cdn_site_role_name == "Market Linear Edge" or cdn_site_role_name == "Regional Internal Edge" or cdn_site_role_name == "Regional Linear Edge" or cdn_site_role_name == "Regional Linear MidTier" or cdn_site_role_name == "Regional VOD" or cdn_site_role_name == "Market VOD":
            base_url = prod_akamai_api_url
            bearer_token = prod_akamai_api_token
        elif cdn_site_role_name == "Spectrum Enterprise HPCs":
            base_url = ent_akamai_api_url
            bearer_token = ent_akamai_api_token
        elif cdn_site_role_name == "Dev_Site":
            base_url = dev_akamai_api_url
            bearer_token = dev_akamai_api_token
        else:
            # Log or handle the unknown role, but don't raise here yet
            self.logger.error(f"Unknown CDN site role encountered: {cdn_site_role_name}")
            # If no token was set, raise an error here
            if bearer_token is None:
                raise ValueError(f"Bearer token not found for the given role: {cdn_site_role_name}")

        # Now bearer_token is either set or you've raised an error if it wasn't
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer_token}",
        }
        # This pulls the entire list of sites so that the neighbor site IDs can be captured
        sites_url = f"{base_url}infrastructure/v1/sites"
        all_sites = requests.get(sites_url, headers=headers, verify=False)

        if all_sites.status_code == 200:
            sites_data = all_sites.json()
            neighbor1_siteid = None
            neighbor2_siteid = None

            for site in sites_data['sites']:
                # Remove 'beta_' prefix from neighbor names before comparison
                neighbor1_name = nb["cdn_site"]["neighbor1"]["name"]
                neighbor1_name = neighbor1_name[5:] if neighbor1_name.startswith('beta_') else neighbor1_name
                
                neighbor2_name = nb["cdn_site"]["neighbor2"]["name"]
                neighbor2_name = neighbor2_name[5:] if neighbor2_name.startswith('beta_') else neighbor2_name

                if site['name'] == neighbor1_name:
                    neighbor1_siteid = site['siteId']
                if site['name'] == neighbor2_name:
                    neighbor2_siteid = site['siteId']

            return neighbor1_siteid, neighbor2_siteid
        else:
            print(f"Request failed with status code {all_sites.status_code}")
            return None, None

    ### Checks to see if the site up for creation already exists
    def site_exists(self, nb, cdn_site_role_name ):
        bearer_token = None

        if cdn_site_role_name == "Beta_Site" or cdn_site_role_name == "Beta_Linear_Edge" or cdn_site_role_name == "Beta Linear Edge":
            base_url = beta_akamai_api_url
            bearer_token = beta_akamai_api_token
            site_name = nb["cdn_site"]["name"]
            site_name = site_name[5:]
        elif cdn_site_role_name == "Market Linear Edge" or cdn_site_role_name == "Regional Internal Edge" or cdn_site_role_name == "Regional Linear Edge" or cdn_site_role_name == "Regional Linear MidTier" or cdn_site_role_name == "Regional VOD" or cdn_site_role_name == "Market VOD":
            base_url = prod_akamai_api_url
            bearer_token = prod_akamai_api_token
            site_name = nb["cdn_site"]["name"]
        elif cdn_site_role_name == "Spectrum Enterprise HPCs":
            base_url = ent_akamai_api_url
            bearer_token = ent_akamai_api_token
            site_name = nb["cdn_site"]["name"]
        elif cdn_site_role_name == "Dev_Site":
            base_url = dev_akamai_api_url
            bearer_token = dev_akamai_api_token
            site_name = nb["cdn_site"]["name"]
        else:
            # Log or handle the unknown role, but don't raise here yet
            self.logger.error(f"Unknown CDN site role encountered: {cdn_site_role_name}")
            # If no token was set, raise an error here
            if bearer_token is None:
                raise ValueError(f"Bearer token not found for the given role: {cdn_site_role_name}")

        # Now bearer_token is either set or you've raised an error if it wasn't
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer_token}",
        }
        
        self.logger.info(f"Received nb_data structure: {nb}")
        
        # This pulls the entire list of sites so that the neighbor site IDs can be captured
        sites_url = f"{base_url}infrastructure/v1/sites"
        all_sites = requests.get(sites_url, headers=headers, verify=False)

        if all_sites.status_code == 200:
            sites_data = all_sites.json()
            for site in sites_data['sites']:
                if site['name'] == site_name:
                    exist_siteId = site['siteId']
                    return True, exist_siteId
            return False, None
        else:
            print(f"Request failed with status code {all_sites.status_code}")

    ### Updates the CDN Site with the new Akamai Site ID
    def update_siteid_with_akamai_siteid(self, site_name, api_site_id):
        """Update the siteId for the CdnSite in Nautobot."""
        try:
            site = CdnSite.objects.get(name=site_name)  # Use name directly
            site.siteId = api_site_id
            site.save()
            self.logger.success(f"Updated site '{site_name}' with Akamai siteId {api_site_id}")
        except CdnSite.DoesNotExist:
            self.logger.error(f"Site '{site_name}' not found in Nautobot.")