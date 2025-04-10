from django_tables2 import RequestConfig
from django.conf import settings
from django.views.generic import TemplateView
from deepmerge import Merger
import json
import requests
from datadog import initialize, api
from html.parser import HTMLParser

from nautobot.core.views import mixins as view_mixins
from nautobot.core.views import generic
from nautobot.core.models.querysets import count_related
from nautobot.extras.views import ObjectChangeLogView, JobResultView 
from nautobot.extras.models import RelationshipAssociation, Relationship
from nautobot.core.views.paginator import EnhancedPaginator, get_paginate_count
from nautobot.dcim.models import Device
from nautobot.dcim.tables import DeviceTable
from nautobot.core.forms import TableConfigForm


from .signals import table_exists
from .models import (
    HyperCacheMemoryProfile,
    SiteRole,
    CdnSite,
    CdnConfigContext
)

from . import ( 
    filters, 
    forms, 
    tables,
)
class HyperCacheMemoryProfileListView(generic.ObjectListView):
    queryset = HyperCacheMemoryProfile.objects.all()
    filterset = filters.HyperCacheMemoryProfileFilterSet
    table = tables.HyperCacheMemoryProfileTable

class HyperCacheMemoryProfileEditView(generic.ObjectEditView):
    queryset = HyperCacheMemoryProfile.objects.all()
    model_form = forms.HyperCacheMemoryProfileForm


class HyperCacheMemoryProfileDeleteView(generic.ObjectDeleteView):
    queryset = HyperCacheMemoryProfile.objects.all()

class HyperCacheMemoryProfileBulkImportView(generic.BulkImportView):
    queryset = HyperCacheMemoryProfile.objects.all()
    model_form = forms.HyperCacheMemoryProfileCSVForm
    table = tables.HyperCacheMemoryProfileTable

class HyperCacheMemoryProfileBulkDeleteView(generic.BulkDeleteView):
    queryset = HyperCacheMemoryProfile.objects.all()
    table = tables.HyperCacheMemoryProfileTable

class SiteRoleView(generic.ObjectView):
    queryset = SiteRole.objects.all()

    def get_extra_context(self, request, instance):
        # CdnSites
        cdnsites = CdnSite.objects.restrict(request.user, "view").filter(
            cdn_site_role__in=instance.descendants(include_self=True)
        )

        cdnsite_table = tables.CdnSiteTable(cdnsites)
        cdnsite_table.columns.hide("cdn_site_role")

        paginate = {
            "paginator_class": EnhancedPaginator,
            "per_page": get_paginate_count(request),
        }
        RequestConfig(request, paginate).configure(cdnsite_table)

        return {
            "cdnsite_table": cdnsite_table,
        }

class SiteRoleListView(generic.ObjectListView):
    queryset = SiteRole.objects.annotate(cdn_site_count=count_related(CdnSite, "cdn_site_role"))
    filterset = filters.SiteRoleFilterSet
    table = tables.SiteRoleTable

class SiteRoleEditView(generic.ObjectEditView):
    queryset = SiteRole.objects.all()
    model_form = forms.SiteRoleForm


class SiteRoleDeleteView(generic.ObjectDeleteView):
    queryset = SiteRole.objects.all()

class SiteRoleBulkImportView(generic.BulkImportView):
    queryset = SiteRole.objects.all()
    model_form = forms.SiteRoleCSVForm
    table = tables.SiteRoleTable

class SiteRoleBulkDeleteView(generic.BulkDeleteView):
    queryset = SiteRole.objects.annotate(cdn_site_count=count_related(CdnSite, "cdn_site_role"))
    table = tables.SiteRoleTable

class CdnSiteListView(generic.ObjectListView):
    queryset = CdnSite.objects.all()
    filterset = filters.CdnSiteFilterSet
    filterset_form = forms.CdnSiteFilterForm
    table = tables.CdnSiteTable


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            for attr in attrs:
                if attr[0] == 'src':
                    self.iframe_src = attr[1]
                           
class CdnSiteView(generic.ObjectView):
    queryset = CdnSite.objects.select_related("location", "cdn_site_role", "status")
    
    def get_extra_context(self, request, instance):
        relationship = Relationship.objects.get(key="cdnsite_devices")

        # Fetch associated Device IDs
        device_ids = RelationshipAssociation.objects.filter(
            relationship=relationship, destination_id=instance.id
        ).values_list("source_id", flat=True)

        # Fetch Device objects
        related_devices = Device.objects.filter(id__in=device_ids)

        # Enable Table Column Customization
        relation_table = DeviceTable(related_devices, user=request.user)

        paginate = {
            "paginator_class": EnhancedPaginator,
            "per_page": get_paginate_count(request),
        }
        RequestConfig(request, paginate).configure(relation_table)

        return {
            "stats": {"device_count": related_devices.count()},
            "relation_table": relation_table,
            "table_config_form": TableConfigForm(relation_table),  # Enable column selection
        }
       
class CdnSiteEditView(generic.ObjectEditView):
    queryset = CdnSite.objects.all()
    model_form = forms.CdnSiteForm
    template_name = "nautobot_cdn_models/cdnsite_edit.html"

class CdnSiteDeleteView(generic.ObjectDeleteView):
    queryset = CdnSite.objects.all()

class CdnSiteBulkImportView(generic.BulkImportView):
    queryset = CdnSite.objects.all()
    model_form = forms.CdnSiteCSVForm
    table = tables.CdnSiteTable

class CdnSiteBulkEditView(generic.BulkEditView):
    queryset = CdnSite.objects.select_related("location", "cdn_site_role")
    filterset = filters.CdnSiteFilterSet
    table = tables.CdnSiteTable
    form = forms.CdnSiteBulkEditForm

class CdnSiteBulkDeleteView(generic.BulkDeleteView):
    queryset = CdnSite.objects.select_related("location", "cdn_site_role")
    filterset = filters.CdnSiteFilterSet
    table = tables.CdnSiteTable

class CdnSiteChangeLogView(ObjectChangeLogView):
    base_template = "nautobot_akamai_models/cdnsite.html"

#
# Config contexts
#

class CdnConfigContextListView(generic.ObjectListView):
    queryset = CdnConfigContext.objects.all()
    filterset = filters.CdnConfigContextFilterSet
    filterset_form = forms.CdnConfigContextFilterForm
    table = tables.CdnConfigContextTable
    action_buttons = ("add",)


class CdnConfigContextView(generic.ObjectView):
    queryset = CdnConfigContext.objects.all()

    def get_extra_context(self, request, instance):
        # Determine user's preferred output format
        if request.GET.get("format") in ["json", "yaml"]:
            format_ = request.GET.get("format")
            if request.user.is_authenticated:
                request.user.set_config("cdnconfigcontext.format", format_, commit=True)
        elif request.user.is_authenticated:
            format_ = request.user.get_config("cdnconfigcontext.format", "json")
        else:
            format_ = "json"

        return {
            "format": format_,
        }

    
class CdnConfigContextEditView(generic.ObjectEditView):
    queryset = CdnConfigContext.objects.all()
    model_form = forms.CdnConfigContextForm
    template_name = "nautobot_cdn_models/cdnconfigcontext_edit.html"


class CdnConfigContextBulkEditView(generic.BulkEditView):
    queryset = CdnConfigContext.objects.all()
    filterset = filters.CdnConfigContextFilterSet
    table = tables.CdnConfigContextTable
    form = forms.CdnConfigContextBulkEditForm


class CdnConfigContextDeleteView(generic.ObjectDeleteView):
    queryset = CdnConfigContext.objects.all()


class CdnConfigContextBulkDeleteView(generic.BulkDeleteView):
    queryset = CdnConfigContext.objects.all()
    table = tables.CdnConfigContextTable


# define a merger with a custom list merge strategy
list_merger = Merger(
    # pass in a list of tuple, with the "strategy" as the first element and the "type" as the second element
    [
        (list, ["append"]),
        (dict, ["merge"])
    ],
    ["override"],
    ["override"]
)

class ObjectCdnConfigContextView(generic.ObjectView):
    base_template = None
    template_name = "nautobot_cdn_models/object_cdnconfigcontext.html"

    def get_extra_context(self, request, instance):
        source_contexts = CdnConfigContext.objects.restrict(request.user, "view").get_for_object(instance)
        # Merge the context data
        merged_data = {}
        for context in source_contexts:
            merged_data = list_merger.merge(merged_data, context.data)

        # Determine user's preferred output format
        if request.GET.get("format") in ["json", "yaml"]:
            format_ = request.GET.get("format")
            if request.user.is_authenticated:
                request.user.set_config("extras.configcontext.format", format_, commit=True)
        elif request.user.is_authenticated:
            format_ = request.user.get_config("extras.configcontext.format", "json")
        else:
            format_ = "json"

        return {
            "rendered_context": instance.get_config_context(),
            "source_contexts": source_contexts,
            "format": format_,
            "base_template": self.base_template,
            "active_tab": "config-context",
        }

class CdnSiteConfigContextView(ObjectCdnConfigContextView):
    def get_queryset(self):
        if not table_exists('dcim_location'):
            print("Location table not available yet, returning empty queryset.")
            return CdnSite.objects.none()
        return CdnSite.objects.annotate_config_context_data()
    base_template = "nautobot_akamai_models/cdnsite.html"
    
### Job Custom Overrides ###
class CustomJobResultView(JobResultView):
    template_name = "nautobot_cdn_models/customized_jobresult.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_result = context.get("object")
        if job_result and job_result.result:
            print(f"Raw job result data: {job_result}")
            context["results"] = job_result.result.get("results", [])
        else:
            context["results"] = []
        context["custom_message"] = "This is my custom job result view."
        return context

override_views = {
    "extras:jobresult": CustomJobResultView.as_view(),
}