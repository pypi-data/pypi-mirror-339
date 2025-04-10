from nautobot.apps.api import NautobotModelSerializer

from nautobot_cdn_models.models import (
    HyperCacheMemoryProfile,
    SiteRole,
    CdnSite,
    CdnConfigContext
)

class HyperCacheMemoryProfileSerializer(NautobotModelSerializer):  # pylint: disable=R0901,too-few-public-methods
    """API serializer."""

    class Meta:
        """Meta attributes."""

        model = HyperCacheMemoryProfile
        fields = "__all__"

class SiteRoleSerializer(NautobotModelSerializer):  # pylint: disable=R0901,too-few-public-methods
    """API serializer."""

    class Meta:
        """Meta attributes."""

        model = SiteRole
        fields = "__all__"

class CdnSiteSerializer(NautobotModelSerializer):  # pylint: disable=R0901,too-few-public-methods
    """API serializer."""

    class Meta:
        """Meta attributes."""

        model = CdnSite
        fields = "__all__"
        

class CdnConfigContextSerializer(NautobotModelSerializer):  # pylint: disable=R0901,too-few-public-methods
    """API serializer."""

    class Meta:
        """Meta attributes."""

        model = CdnConfigContext
        fields = "__all__"