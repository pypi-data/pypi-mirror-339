from rest_framework import routers

from nautobot_cdn_models.api.views import (
    HyperCacheMemoryProfileView,
    SiteRoleView,
    CdnSiteView,
    CdnConfigContextView
)

router = routers.DefaultRouter()
router.register("hypercachememoryprofiles", HyperCacheMemoryProfileView)
router.register("siteroles", SiteRoleView)
router.register("cdnsites", CdnSiteView)
router.register("cdnconfigcontexts", CdnConfigContextView)

app_name = "nautobot_cdn_models"  # pylint: disable=invalid-name

urlpatterns = router.urls