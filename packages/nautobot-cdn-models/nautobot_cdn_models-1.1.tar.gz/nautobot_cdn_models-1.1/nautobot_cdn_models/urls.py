from django.urls import path, include
from django.templatetags.static import static
from django.views.generic import RedirectView

from nautobot.apps.urls import NautobotUIViewSetRouter
from nautobot.extras.views import ObjectNotesView
from nautobot_cdn_models import views, viewsets
from nautobot_cdn_models.models import (
    CdnConfigContext,
    SiteRole,
    CdnSite
)

app_name = "nautobot_cdn_models"

router = NautobotUIViewSetRouter()
router.register("hypercachememoryprofiles", viewset=viewsets.HyperCacheMemoryProfileUIViewSet)
router.register("siteroles", viewset=viewsets.SiteRoleUIViewSet)
# router.register("cdnsites", viewset=viewsets.CdnSiteUIViewSet)
# router.register("serviceproviders", views.ServiceProviderUIViewSet)
# router.register("contentproviders", views.ContentProviderUIViewSet)
# router.register("origins", views.OriginUIViewSet)
# router.register("cdnprefix", views.CdnPrefixUIViewSet)
# router.register("cdnprefixdefaultbehavior", views.CdnPrefixDefaultBehaviorUIViewSet)
# router.register("cdnprefixbehavior", views.CdnPrefixBehaviorUIViewSet)

urlpatterns = [

    path("cdnsites/", views.CdnSiteListView.as_view(), name="cdnsite_list"),
    path("cdnsites/add/", views.CdnSiteEditView.as_view(), name="cdnsite_add"),
    path("cdnsites/import/", views.CdnSiteBulkImportView.as_view(), name="cdnsite_import"),
    path("cdnsites/edit/", views.CdnSiteBulkEditView.as_view(), name="cdnsite_bulk_edit"),
    path("cdnsites/delete/", views.CdnSiteBulkDeleteView.as_view(), name="cdnsite_bulk_delete"),
    path("cdnsites/<uuid:pk>/", views.CdnSiteView.as_view(), name="cdnsite"),
    path("cdnsites/<uuid:pk>/edit/", views.CdnSiteEditView.as_view(), name="cdnsite_edit"),
    path("cdnsites/<uuid:pk>/delete/", views.CdnSiteDeleteView.as_view(), name="cdnsite_delete"),
    path("cdnsites/<uuid:pk>/cdn-config-context/", views.CdnSiteConfigContextView.as_view(), name="cdnsite_cdnconfigcontext"),
    path("cdnsites/<uuid:pk>/notes/",ObjectNotesView.as_view(),name="cdnsite_notes",kwargs={"model": CdnSite}),
    
    # Config contexts
    path("cdnconfig-contexts/", views.CdnConfigContextListView.as_view(), name="cdnconfigcontext_list",),
    path("cdnconfig-contexts/add/", views.CdnConfigContextEditView.as_view(), name="cdnconfigcontext_add",),
    path("cdnconfig-contexts/edit/", views.CdnConfigContextBulkEditView.as_view(), name="cdnconfigcontext_bulk_edit",),
    path("cdnconfig-contexts/delete/", views.CdnConfigContextBulkDeleteView.as_view(), name="cdnconfigcontext_bulk_delete",),
    path("cdnconfig-contexts/<uuid:pk>/", views.CdnConfigContextView.as_view(), name="cdnconfigcontext",),
    path("cdnconfig-contexts/<uuid:pk>/edit/", views.CdnConfigContextEditView.as_view(), name="cdnconfigcontext_edit",),
    path("cdnconfig-contexts/<uuid:pk>/delete/", views.CdnConfigContextDeleteView.as_view(), name="cdnconfigcontext_delete",),
    path("cdnconfig-contexts/<uuid:pk>/changelog/", views.ObjectChangeLogView.as_view(), name="cdnconfigcontext_changelog", kwargs={"model": CdnConfigContext},),
    path("cdnconfig-contexts/<uuid:pk>/notes/", ObjectNotesView.as_view(), name="cdnconfigcontext_notes", kwargs={"model": CdnConfigContext},),
    
    path("docs/", RedirectView.as_view(url="http://localhost:8001/projects/cdn-models/en/latest/"), name="docs"),
    
    path("verifybgp-results/<uuid:pk>/", views.CustomJobResultView.as_view(), name="custom_job_result"),
]
urlpatterns += router.urls