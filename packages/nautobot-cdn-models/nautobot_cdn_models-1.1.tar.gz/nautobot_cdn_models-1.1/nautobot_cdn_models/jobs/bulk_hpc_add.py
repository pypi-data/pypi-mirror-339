import re
from django.contrib.contenttypes.models import ContentType
from nautobot.apps.jobs import Job, IntegerVar, ObjectVar, BooleanVar, StringVar
from nautobot.dcim.models import Device, DeviceType, Platform, Manufacturer, Location
from nautobot.extras.models import Status, Relationship, RelationshipAssociation, Role
from nautobot_cdn_models.models import CdnSite, SiteRole


name = "Akamai CDN Tools"
class NewHpcs(Job):

    class Meta:
        name = "Bulk Add New Hypercaches"
        description = "Create new Hypercache devices in Nautobot"
        field_order = ["site_name", "manufacturer", "hpc_model", "cdnsite_name"]

    site_name = ObjectVar(
        description="Location of the new HPCs",
        model=Location
    )
    
    manufacturer = ObjectVar(
        description="Filter Device Type by Manufacturer",
        model=Manufacturer
    )
    
    hpc_model = ObjectVar(
        description="Hypercache server model",
        model=DeviceType,
        query_params={"manufacturer": "$manufacturer"},
        required=True
    )
    
    role = ObjectVar(
        model=Role,
        required=True
    )
    
    count = IntegerVar(
        description="Number of devices to add",
        default=1
    )
    
    platform = ObjectVar(
        model=Platform,
        description="Select the platform for the device",
        query_params={"manufacturer": "$manufacturer"},
        required=True
    )
    
    cdnsite_name = ObjectVar(
        model=CdnSite,
        description="Assign new HPCs to an existing site",
        query_params={"location": "$site_name"},
        required=False
    )
    
    commit = BooleanVar(
        description:="UnCheck this Box to perform a dryrun for testing",
        default=True
    )

    def run(self, *args, **kwargs):
        STATUS_PLANNED = Status.objects.get(name="Planned")
        SITE = kwargs['site_name']

        city = SITE.name.split('_')[0].capitalize()
        clli = SITE.name.split('_')[1]
        
        physical_address = SITE.physical_address or ""
        state_code = self.extract_state_from_address(physical_address)
        if not state_code:
            self.logger.warning(f"Could not extract state from address: {physical_address}. Falling back to CLLI-derived state.")
            state_code = clli[-2:].upper()
        
        if kwargs['role'].name in ["linear_pop_edge", "linear_mid_tier", "linear_shield_cache"]:
            base_number = 1000
        elif kwargs['role'].name in ["vod_edge_cache", "vod_shield_cache"]:
            base_number = 0
        else:
            base_number = 1000
        
        if kwargs['role'].name == "linear_c_hub":
            if Device.objects.filter(location=SITE, role__name="linear_pop_edge").exists():
                if any(d.name.startswith(f"{clli}-ak-hpc1") for d in Device.objects.filter(location=SITE)):
                    base_number = 1100
            else:
                base_number = 1000
        
        existing_devices = Device.objects.filter(location=SITE)
        
        numbers = []
        for device in existing_devices:
            for prefix in ['hpc', 'mid', 'shc']:
                if prefix in device.name:
                    parts = device.name.split(prefix)[1].split('.')
                    if parts:
                        try:
                            num = int(parts[0])
                            if base_number == 1100 and num < 1100:
                                continue
                            numbers.append(num)
                        except ValueError:
                            self.logger.warning(f"Could not convert device name part to integer: {device.name}")
                    break

        next_num = base_number + 1 if not numbers else max(numbers) + 1
        
        new_devices = []
        for _ in range(kwargs['count']):
            if kwargs['role'].name in ["linear_c_hub", "linear_pop_edge"]:
                device_name = f"{clli}-ak-hpc{next_num}.spectrum.com"
            elif kwargs['role'].name == "linear_mid_tier":
                device_name = f"{clli}-ak-mid{next_num}.spectrum.com"
            elif kwargs['role'].name == "linear_shield_cache":
                device_name = f"{clli}-ak-shc{next_num}.spectrum.com"
            elif kwargs['role'].name == "vod_edge_cache":
                device_name = f"{clli}-ak-hpc000{next_num}.spectrum.com"
            elif kwargs['role'].name == "vod_shield_cache":
                device_name = f"{clli}-ak-shc000{next_num}.spectrum.com"
            else:
                device_name = f"{clli}-ak-hpc{next_num}.spectrum.com"
            
            device = Device(
                name=device_name,
                role=kwargs['role'],
                location=SITE,
                platform=kwargs['platform'],
                device_type=kwargs['hpc_model'],
                status=STATUS_PLANNED,
            )
            new_devices.append(device)
            next_num += 1
        
        if not kwargs['cdnsite_name']:
            region = SITE.parent
            if kwargs['role'].name == "linear_c_hub":
                site_role = SiteRole.objects.get(name="Market Linear Edge")
                site_name = f"{region}_{city}_{state_code}_linear_hpc"
                abbrev = f"{clli}_l_hpc"
            elif kwargs['role'].name == "linear_pop_edge":
                site_role = SiteRole.objects.get(name="Regional Linear Edge")
                site_name = f"{region}_{city}-POP_{state_code}_linear_hpc"
                abbrev = f"{clli}_l_hpc"
            elif kwargs['role'].name == "linear_mid_tier":
                site_role = SiteRole.objects.get(name="Regional Linear MidTier")
                site_name = f"{region}_{city}-POP_{state_code}_linear_mid"
                abbrev = f"{clli}_l_mid"
            elif kwargs['role'].name == "linear_shield_cache":
                site_role = SiteRole.objects.get(name="Linear-Shields")
                site_name = f"{region}_{city}_{state_code}_linear_shield"
                abbrev = f"{clli}_l_mid"
            elif kwargs['role'].name == "vod_edge_cache":
                site_role = SiteRole.objects.get(name="Regional Vod Edge")
                site_name = f"{region}_{city}-POP_{state_code}_vod_hpc"
                abbrev = f"{clli}_v_hpc"
            elif kwargs['role'].name == "vod_shield_cache":
                site_role = SiteRole.objects.get(name="VOD-Shields")
                site_name = f"{region}_{city}_{state_code}_vod_shield"
                abbrev = f"{clli}_v_shc"
            else:
                site_role = SiteRole.objects.get(name="Market Linear Edge")
                site_name = f"{region}_{city}_{state_code}_linear_hpc"
                abbrev = f"{clli}_l_hpc"
            
            new_cdnsite = CdnSite(
                name=site_name,
                abbreviatedName=abbrev,
                cdn_site_role=site_role,
                location=SITE,
                status=STATUS_PLANNED,
            )

            if kwargs.get('commit', False):
                new_cdnsite.save()
                self.logger.info(f"Created new SITE: {new_cdnsite}")
            else:
                self.logger.info(f"No commit, DryRun: {new_cdnsite}")
            
        for device in new_devices:
            if kwargs.get('commit', False):
                device.save()
                self.logger.info(f"Created new hpc: {device}")
                
                # Associate with either the provided cdnsite_name or the newly created cdnsite
                target_cdnsite = kwargs.get('cdnsite_name') or new_cdnsite
                if target_cdnsite:
                    try:
                        relationship = Relationship.objects.get(label="CdnSite's Associated Devices")
                        RelationshipAssociation.objects.create(
                            relationship=relationship,
                            source_type=ContentType.objects.get_for_model(Device),
                            source_id=device.id,
                            destination_type=ContentType.objects.get_for_model(CdnSite),
                            destination_id=target_cdnsite.id 
                        )
                        self.logger.info(f"Associated device {device.name} with CDN site {target_cdnsite.name}")
                    except Relationship.DoesNotExist:
                        self.logger.error("Relationship 'cdnsite-device' does not exist.")
            else:
                self.logger.info(f"No commit, DryRun: {device}")
                
    def extract_state_from_address(self, address):
        """Extract the two-letter state code from a physical address."""
        if not address:
            return None
        # Example address: "21692 COUNTY ROAD 54 ALBANY MN 56307"
        # Use regex to find two uppercase letters before the ZIP code
        match = re.search(r'\b([A-Z]{2})\b\s+\d{5}', address)
        if match:
            return match.group(1)
        # Fallback: split by spaces and look for a two-letter code
        parts = address.split()
        for part in parts:
            if len(part) == 2 and part.isalpha() and part.isupper():
                return part
        return None