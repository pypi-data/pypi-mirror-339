"""Menu items for the CDN Models app."""
# pylint: disable=C0412
from nautobot.core.apps import NavMenuButton, NavMenuGroup, NavMenuItem, NavMenuTab
from nautobot.core.choices import ButtonColorChoices

menu_items = (
    NavMenuTab(
        name=" LCDN",
        weight=100,
        groups=(
            NavMenuGroup(
                name=" Site Configurations",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_cdn_models:hypercachememoryprofile_list",
                        name="HyperCache Memory Profiles",
                        buttons=(
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:hypercachememoryprofile_add",
                                title="Add",
                                icon_class="mdi mdi-plus-thick",
                                button_class=ButtonColorChoices.GREEN,
                                permissions=[
                                    "nautobot_cdn_models.add_hypercachememoryprofile",
                                ],
                            ),
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:hypercachememoryprofile_import",
                                title="Import",
                                icon_class="mdi mdi-database-import-outline",
                                button_class=ButtonColorChoices.BLUE,
                                permissions=[
                                    "nautobot_cdn_models.add_hypercachememoryprofile",
                                ],
                            ),
                        ),
                        permissions=[
                            "nautobot_cdn_models.view_hypercachememoryprofiles"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_cdn_models:siterole_list",
                        name=" Site Roles",
                        buttons=(
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:siterole_add",
                                title="Add",
                                icon_class="mdi mdi-plus-thick",
                                button_class=ButtonColorChoices.GREEN,
                                permissions=[
                                    "nautobot_cdn_models.add_siterole",
                                ],
                            ),
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:siterole_import",
                                title="Import",
                                icon_class="mdi mdi-database-import-outline",
                                button_class=ButtonColorChoices.BLUE,
                                permissions=[
                                    "nautobot_cdn_models.add_siterole",
                                ],
                            ),
                        ),
                        permissions=[
                            "nautobot_cdn_models.view_siteroles"
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_cdn_models:cdnsite_list",
                        name=" Sites Configuration",
                        buttons=(
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:cdnsite_add",
                                title="Add",
                                icon_class="mdi mdi-plus-thick",
                                button_class=ButtonColorChoices.GREEN,
                                permissions=[
                                    "nautobot_cdn_models.add_cdnsite"
                                ],
                            ),
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:cdnsite_import",
                                title="Import",
                                icon_class="mdi mdi-database-import-outline",
                                button_class=ButtonColorChoices.BLUE,
                                permissions=[
                                    "nautobot_cdn_models.add_cdnsite"
                                ],
                            ),
                        ),
                        permissions=[
                            "nautobot_cdn_models.view_cdnsites"
                        ],
                    ),
                ),
            ),
            NavMenuGroup(
                name=" Redirect Maps",
                weight=150,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_cdn_models:cdnconfigcontext_list",
                        name="Redirect Map Contexts",
                        buttons=(
                            NavMenuButton(
                                link="plugins:nautobot_cdn_models:cdnconfigcontext_add",
                                title="Add",
                                icon_class="mdi mdi-plus-thick",
                                button_class=ButtonColorChoices.GREEN,
                                permissions=[
                                    "nautobot_cdn_models.add_cdnconfigcontext"
                                ],
                            ),
                        ),
                        permissions=[
                            "nautobot_cdn_models.view_cdnconfigcontexts"
                            ],
                    ),
                ),
            ),
        ),
    ),
)
