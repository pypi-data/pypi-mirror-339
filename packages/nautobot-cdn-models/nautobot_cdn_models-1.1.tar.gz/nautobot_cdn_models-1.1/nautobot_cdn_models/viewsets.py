from nautobot.apps.views import NautobotUIViewSet

from nautobot_cdn_models import filters, forms, models, tables
from nautobot_cdn_models.api import serializers

class HyperCacheMemoryProfileUIViewSet(NautobotUIViewSet):
    bulk_update_form_class = forms.HyperCacheMemoryProfileBulkEditForm
    filterset_class = filters.HyperCacheMemoryProfileFilterSet
    filterset_form_class = forms.HyperCacheMemoryProfileFilterForm
    form_class = forms.HyperCacheMemoryProfileForm
    queryset = models.HyperCacheMemoryProfile.objects.all()
    serializer_class = serializers.HyperCacheMemoryProfileSerializer
    table_class = tables.HyperCacheMemoryProfileTable


class SiteRoleUIViewSet(NautobotUIViewSet):
    filterset_class = filters.SiteRoleFilterSet
    filterset_form_class = forms.SiteRoleFilterForm
    form_class = forms.SiteRoleForm
    queryset = models.SiteRole.objects.all()
    serializer_class = serializers.SiteRoleSerializer
    table_class = tables.SiteRoleTable


class CdnSiteUIViewSet(NautobotUIViewSet):
    bulk_update_form_class = forms.CdnSiteBulkEditForm
    filterset_class = filters.CdnSiteFilterSet
    filterset_form_class = forms.CdnSiteFilterForm
    form_class = forms.CdnSiteForm
    queryset = models.CdnSite.objects.all()
    serializer_class = serializers.CdnSiteSerializer
    table_class = tables.CdnSiteTable