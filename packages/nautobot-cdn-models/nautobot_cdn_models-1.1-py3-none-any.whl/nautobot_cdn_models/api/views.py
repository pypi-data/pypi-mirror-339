from nautobot.apps.api import NautobotModelViewSet

from nautobot_cdn_models.models import (
    HyperCacheMemoryProfile,
    SiteRole,
    CdnSite,
    CdnConfigContext
)

from nautobot_cdn_models import ( 
    filters
)

from nautobot_cdn_models.api.serializers import (
    HyperCacheMemoryProfileSerializer,
    SiteRoleSerializer,
    CdnSiteSerializer,
    CdnConfigContextSerializer
)

class HyperCacheMemoryProfileView(NautobotModelViewSet):
    """CRUD operations set for the Hardware Lifecycle Management view."""

    queryset = HyperCacheMemoryProfile.objects.all()
    filterset_class = filters.HyperCacheMemoryProfileFilterSet
    serializer_class = HyperCacheMemoryProfileSerializer

class SiteRoleView(NautobotModelViewSet):
    """CRUD operations set for the Hardware Lifecycle Management view."""

    queryset = SiteRole.objects.all()
    filterset_class = filters.SiteRoleFilterSet
    serializer_class = SiteRoleSerializer

class CdnSiteView(NautobotModelViewSet):
    """CRUD operations set for the Hardware Lifecycle Management view."""

    queryset = CdnSite.objects.all()
    filterset_class = filters.CdnSiteFilterSet
    serializer_class = CdnSiteSerializer

class CdnConfigContextView(NautobotModelViewSet):
    """CRUD operations set for the Hardware Lifecycle Management view."""

    queryset = CdnConfigContext.objects.all()
    filterset_class = filters.CdnConfigContextFilterSet
    serializer_class = CdnConfigContextSerializer