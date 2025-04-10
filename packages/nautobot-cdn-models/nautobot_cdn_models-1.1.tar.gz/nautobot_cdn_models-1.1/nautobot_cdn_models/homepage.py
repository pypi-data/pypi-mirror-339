from nautobot.core.apps import HomePageGroup, HomePageItem, HomePagePanel
from nautobot_cdn_models.models import (
    HyperCacheMemoryProfile,
    SiteRole,
    CdnSite,
    CdnConfigContext,
)

layout = (
    HomePagePanel(
        name=" LCDN",
        weight=600,
        items=(
            HomePageGroup(
                name=" Site Configurations",
                weight=100,
                items=(
                    HomePageItem(
                        name=" HyperCache Memory Profiles",
                        link="plugins:nautobot_cdn_models:hypercachememoryprofile_list",
                        model=HyperCacheMemoryProfile,
                        description=" Site Hypercache Memory Profiles",
                        permissions=["nautobot_cdn_models.view_hypercachememoryprofiles"],
                        weight=100,
                    ),
                    HomePageItem(
                        name=" Site Roles",
                        link="plugins:nautobot_cdn_models:siterole_list",
                        model=SiteRole,
                        description=" LCDN Site Groupings",
                        permissions=["nautobot_cdn_models.view_siteroles"],
                        weight=150,
                    ),
                    HomePageItem(
                        name=" Site Configuration",
                        link="plugins:nautobot_cdn_models:cdnsite_list",
                        model=CdnSite,
                        description=" Site Configuration Source of Truth",
                        permissions=["nautobot_cdn_models.view_cdnsites"],
                        weight=200,
                    ),
                ),
            ),
            HomePageGroup(
                name=" Redirect Map Configurations",
                weight=150,
                items=(
                    HomePageItem(
                        name=" Site Redirect Map Context",
                        link="plugins:nautobot_cdn_models:cdnconfigcontext_list",
                        model=CdnConfigContext,
                        description=" Redirect Map Configuration",
                        permissions=["nautobot_cdn_models.view_cdnconfigcontexts"],
                        weight=250,
                    ),
                ),
            ),
            # HomePageGroup(
            #     name=" Content Delivery Configurations",
            #     weight=200,
            #     items=(
            #         HomePageItem(
            #             name=" Service Providers",
            #             link="plugins:nautobot_cdn_models:serviceprovider_list",
            #             model=ServiceProvider,
            #             description=" Service Prodiver Configuration",
            #             permissions=[],
            #             weight=300,
            #         ),
            #         HomePageItem(
            #             name=" Content Providers",
            #             link="plugins:nautobot_cdn_models:contentprovider_list",
            #             model=ContentProvider,
            #             description=" Content Prodiver Configuration",
            #             permissions=[],
            #             weight=350,
            #         ),
            #         HomePageItem(
            #             name=" Origins",
            #             link="plugins:nautobot_cdn_models:origin_list",
            #             model=Origin,
            #             description=" Origin Configuration",
            #             permissions=[],
            #             weight=400,
            #         ),
            #         HomePageItem(
            #             name=" Prefixes",
            #             link="plugins:nautobot_cdn_models:cdnprefix_list",
            #             model=CdnPrefix,
            #             description=" Prefix Configuration",
            #             permissions=[],
            #             weight=450,
            #         ),
            #         HomePageItem(
            #             name=" Prefix Behaviors",
            #             link="plugins:nautobot_cdn_models:cdnprefixbehavior_list",
            #             model=CdnPrefix,
            #             description=" Prefix Behavior rules",
            #             permissions=[],
            #             weight=450,
            #         ),
            #         HomePageItem(
            #             name=" Prefix Default Behaviors",
            #             link="plugins:nautobot_cdn_models:cdnprefixdefaultbehavior_list",
            #             model=CdnPrefix,
            #             description=" Prefix Default Behavior rules",
            #             permissions=[],
            #             weight=450,
            #         ),
            #     ),
            # ),
        ),
    ),
)