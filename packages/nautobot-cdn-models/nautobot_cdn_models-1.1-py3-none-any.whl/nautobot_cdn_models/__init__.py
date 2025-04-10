"""App declaration for nautobot_cdn_models."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig
from nautobot.core.signals import nautobot_database_ready

__version__ = metadata.version(__name__)

class NautobotCdnModelsConfig(NautobotAppConfig):
    """App configuration for the nautobot_cdn_models app."""

    name = "nautobot_cdn_models"
    verbose_name = "Nautobot Cdn Models"
    version = __version__
    author = "Byrn Baker"
    description = "Nautobot Cdn Models."
    base_url = "nautobot-cdn-models"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        "default_statuses": {
            "CdnSite": [
                "Active", 
                "Maintenance", 
                "Planned", 
                "Staged", 
                "Decommissioned", 
                "Moved to next phase"
            ],
        }

    }
    docs_view_name = "plugins:nautobot_cdn_models:docs"
    
    def ready(self):
        """Register custom signals."""        
        import nautobot_cdn_models.signals
        
        nautobot_database_ready.connect(nautobot_cdn_models.signals.post_migrate_create_statuses, sender=self)
        nautobot_database_ready.connect(nautobot_cdn_models.signals.post_migrate_create_relationships, sender=self)
        
        super().ready()


config = NautobotCdnModelsConfig  # pylint:disable=invalid-name