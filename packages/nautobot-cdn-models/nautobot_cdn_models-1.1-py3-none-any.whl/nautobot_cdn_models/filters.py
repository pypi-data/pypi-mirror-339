import django_filters
from django.db import models


from nautobot.extras.filters.mixins import (
    LocalContextModelFilterSetMixin,
    StatusModelFilterSetMixin,
)

from nautobot.extras.filters import (
    NautobotFilterSet,
    LocalContextModelFilterSetMixin,
    StatusModelFilterSetMixin,
)
from nautobot.core.filters import (
    BaseFilterSet,
    ContentTypeFilter,
    NaturalKeyOrPKMultipleChoiceFilter,
    SearchFilter,
    TreeNodeMultipleChoiceFilter,
)
from nautobot.extras.models import ConfigContextSchema
from nautobot.dcim.models import Location
from . import models

class HyperCacheMemoryProfileFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )
    class Meta:
        model = models.HyperCacheMemoryProfile
        fields = "__all__"

class SiteRoleFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )
    class Meta:
        model = models.SiteRole
        fields = "__all__"

class CdnSiteFilterSet(NautobotFilterSet, LocalContextModelFilterSetMixin, StatusModelFilterSetMixin):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )
    location_id = TreeNodeMultipleChoiceFilter(
        queryset=Location.objects.all(),
        field_name="location",
        label="Location (ID)",
    )
    location = TreeNodeMultipleChoiceFilter(
        queryset=Location.objects.all(),
        field_name="location",
        label="Location (name or ID)",
    )
    cdn_site_role = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.SiteRole.objects.all(),
        label="Site Role (name or ID)"
    )
    cacheMemoryProfileId = django_filters.ModelChoiceFilter(
        field_name='name',
        to_field_name='name',
        queryset=models.HyperCacheMemoryProfile.objects.all(),
    )
    class Meta:
        model = models.CdnSite
        fields = [
        "name",
        "abbreviatedName",
        "bandwidthLimitMbps",
        "enableDisklessMode",
        "siteId",
        "cdn_site_role",
        "location",
        "cacheMemoryProfileId",
        "neighbor1",
        "neighbor1_preference",
        "neighbor2",
        "neighbor2_preference",
        'failover_site',
    ]

#
# Config Contexts
#


class CdnConfigContextFilterSet(BaseFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "data": "icontains",
        },
    )
    owner_content_type = ContentTypeFilter()
    schema = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="schema",
        queryset=ConfigContextSchema.objects.all(),
        to_field_name="slug",
        label="Schema (slug or PK)",
    )
    location_id = django_filters.ModelMultipleChoiceFilter(
        field_name="locations",
        queryset=Location.objects.all(),
        label="Location (ID) - Deprecated (use location filter)",
    )
    location = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="locations",
        queryset=Location.objects.all(),
        label="Location (ID or slug)",
    )
    cdnsite_id = django_filters.ModelMultipleChoiceFilter(
        field_name="cdnsites",
        queryset=models.CdnSite.objects.all(),
        label="Site (ID) - Deprecated (use site filter)",
    )
    cdnsite = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="cdnsites",
        queryset=models.CdnSite.objects.all(),
        label="Site (ID or slug)",
    )
    # cdn_site_role_id = django_filters.ModelMultipleChoiceFilter(
    #     field_name="siteroles",
    #     queryset=models.SiteRole.objects.all(),
    #     label="Role (ID) - Deprecated (use role filter)",
    # )
    cdn_site_role = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="siteroles",
        queryset=models.SiteRole.objects.all(),
        label="Role (ID or slug)",
    )

    # Conditional enablement of dynamic groups filtering
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = models.CdnConfigContext
        fields = ["id", "name", "is_active", "owner_content_type", "owner_object_id"]


#
# Content Delivery
#

# class ServiceProviderFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.ServiceProvider
#         fields = "__all__"

# class ContentProviderFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.ContentProvider
#         fields = "__all__"

# class OriginFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.Origin
#         fields = [
#             'name',
#             'contentProviderId',
#             'enable',
#             'originTimeout',
#         ]

# class CdnPrefixFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.CdnPrefix
#         fields = "__all__"
        
# class CdnPrefixDefaultBehaviorFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.CdnPrefixDefaultBehavior
#         fields = "__all__"

# class CdnPrefixBehaviorFilterSet(NautobotFilterSet):
#     q = SearchFilter(
#         filter_predicates={
#             "name": "icontains",
#         },
#     )
#     class Meta:
#         model = models.CdnPrefixBehavior
#         fields = "__all__"