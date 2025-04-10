"""Nautobot signal handler functions for nautobot_cdn_models."""

from django.apps import apps as global_apps
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from nautobot.extras.choices import RelationshipTypeChoices
from nautobot.extras.models import Relationship, RelationshipAssociation
from django.db import connections

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_cdn_models"]

def table_exists(table_name):
    """Check if a specific table exists in the database."""
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE tablename = %s", [table_name])
        return cursor.fetchone()[0] > 0

def post_migrate_create_statuses(sender, *, apps=global_apps, **kwargs):
    """Callback function for post_migrate() -- create default Statuses if the status table exists."""
    # pylint: disable=invalid-name
    if not apps:
        return

    if not table_exists('extras_status'):
        print("Status table does not exist, skipping status creation.")
        return

    Status = apps.get_model("extras", "Status")

    for model_name, default_statuses in PLUGIN_SETTINGS.get("default_statuses", {}).items():
        model = sender.get_model(model_name)

        if not table_exists('contenttypes_contenttype'):
            print(f"Content Type table does not exist for model {model_name}, skipping.")
            continue

        ContentType = apps.get_model("contenttypes", "ContentType")
        ct_model = ContentType.objects.get_for_model(model)
        for status_name in default_statuses:
            try:
                status = Status.objects.get(name=status_name)
            except Status.DoesNotExist:
                print(f"nautobot_cdn_models: Unable to find status: {status_name} .. SKIPPING")
                continue

            if ct_model not in status.content_types.all():
                status.content_types.add(ct_model)
                status.save()

def post_migrate_create_relationships(sender, apps=global_apps, **kwargs):  # pylint: disable=unused-argument
    """Create Relationship records for your Nautobot CDN Models if related tables exist."""
    # pylint: disable=invalid-name
    if not table_exists('extras_relationship'):
        print("Relationship table does not exist, skipping relationship creation.")
        return

    CdnSite = sender.get_model("CdnSite")
    if not table_exists('contenttypes_contenttype'):
        print("Content Type table does not exist, skipping relationship creation.")
        return

    ContentType = apps.get_model("contenttypes", "ContentType")
    _Device = apps.get_model("dcim", "Device")
    _Relationship = apps.get_model("extras", "Relationship")
    _VirtualMachine = apps.get_model("virtualization", "VirtualMachine")

    if not (_Device or _VirtualMachine):
        print("Required models for relationships do not exist, skipping relationship creation.")
        return

    # Create your relationships here   
    for relationship_dict in [
        {
            "label": "CdnSite's Associated Devices",
            "key": "cdnsite_devices",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(CdnSite),
            "source_label": "CdnSite associated to devices",
            "destination_type": ContentType.objects.get_for_model(_Device),
            "destination_label": "Devices associated with a CdnSite",
        },
        {
            "label": "Software on InventoryItem",
            "key": "inventory_item_soft",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(CdnSite),
            "source_label": "CdnSite to associated VMs",
            "destination_type": ContentType.objects.get_for_model(_VirtualMachine),
            "destination_label": "VMs associated with a CdnSite",
        },
    ]:
        _Relationship.objects.get_or_create(label=relationship_dict["label"], defaults=relationship_dict)

@receiver(pre_delete, sender="nautobot_cdn_models.CdnSite")
def delete_cdnsite_devices_relationships(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """Delete all CdnSite relationships to Device objects if the relationship table exists."""
    if not table_exists('extras_relationship'):
        print("Relationship table does not exist, skipping relationship deletion.")
        return

    cdnsite_relationships = Relationship.objects.filter(key__in=("cdnsite_devices"))
    RelationshipAssociation.objects.filter(relationship__in=cdnsite_relationships, source_id=instance.pk).delete()

@receiver(pre_delete, sender="nautobot_cdn_models.CdnSite")
def delete_cdnsite_vms_relationships(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """Delete all CdnSite relationships to VM objects if the relationship table exists. Note: there was a duplicate function name in the original code."""
    if not table_exists('extras_relationship'):
        print("Relationship table does not exist, skipping relationship deletion.")
        return

    cdnsite_relationships = Relationship.objects.filter(key__in=("cdnsite_vms"))
    RelationshipAssociation.objects.filter(relationship__in=cdnsite_relationships, source_id=instance.pk).delete()