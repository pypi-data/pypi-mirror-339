from nautobot.apps.ui import TemplateExtension
from nautobot_cdn_models.models import CdnSite  # Make sure this import is correct based on your model's name and location

class DeviceCdnSiteExtension(TemplateExtension):  # pylint: disable=abstract-method
    """Add CDN site information as a new tab on the Device view."""

    model = "dcim.device"

    def tabs(self):
        """Add a new tab for CDN site information."""
        return self.render(
            "nautobot_cdn_models/inc/device_cdn_site_tab.html",
            extra_context={
                "cdn_sites": self.context["object"].cdn_sites.all(),  # Adjust based on your relationship setup
            },
        )

template_extensions = [DeviceCdnSiteExtension]