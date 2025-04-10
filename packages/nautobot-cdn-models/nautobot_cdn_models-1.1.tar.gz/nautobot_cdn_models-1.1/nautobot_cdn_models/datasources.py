from collections import defaultdict
import logging
import os



from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import transaction
import yaml

from nautobot.dcim.models import Location
from nautobot.extras.choices import (
    LogLevelChoices,
)
from nautobot.extras.models import (
    ConfigContextSchema,
    GitRepository,
    Tag,
)
from nautobot.extras.registry import DatasourceContent, register_datasource_contents

from .models import CdnSite, SiteRole, CdnConfigContext

logger = logging.getLogger(__name__)

def refresh_git_cdn_config_contexts(repository_record, job_result, delete=False):
    """Callback function for GitRepository updates - refresh all ConfigContext records managed by this repository."""
    if "extras.configcontext" in repository_record.provided_contents and not delete:
        update_git_cdn_config_contexts(repository_record, job_result)
    else:
        delete_git_cdn_config_contexts(repository_record, job_result)


def update_git_cdn_config_contexts(repository_record, job_result):
    """Refresh any cdn config contexts provided by this Git repository."""
    cdn_config_context_path = os.path.join(repository_record.filesystem_path, "cdn_config_contexts")
    if not os.path.isdir(cdn_config_context_path):
        return

    managed_cdn_config_contexts = set()
    managed_local_cdn_config_contexts = defaultdict(set)

    # First, handle the "flat file" case - data files in the root cdn_config_context_path,
    # whose metadata is expressed purely within the contents of the file:
    for file_name in os.listdir(cdn_config_context_path):
        if not os.path.isfile(os.path.join(cdn_config_context_path, file_name)):
            continue
        msg = f"Loading config context from `{file_name}`"
        logger.info(msg)
        job_result.log(msg, grouping="cdn config contexts")
        try:
            with open(os.path.join(cdn_config_context_path, file_name), "r") as fd:
                # The data file can be either JSON or YAML; since YAML is a superset of JSON, we can load it regardless
                context_data = yaml.safe_load(fd)

            # A file can contain one config context dict or a list thereof
            if isinstance(context_data, dict):
                context_name = import_cdn_config_context(context_data, repository_record, job_result)
                managed_cdn_config_contexts.add(context_name)
            elif isinstance(context_data, list):
                for context_data_entry in context_data:
                    context_name = import_cdn_config_context(context_data_entry, repository_record, job_result)
                    managed_cdn_config_contexts.add(context_name)
            else:
                raise RuntimeError("data must be a dict or list of dicts")

        except Exception as exc:
            msg = f"Error in loading config context data from `{file_name}`: {exc}"
            logger.error(msg)
            job_result.log(msg, level_choice=LogLevelChoices.LOG_ERROR, grouping="cdn config contexts")

    # Next, handle the "filter/name" directory structure case - files in <filter_type>/<name>.(json|yaml)
    for filter_type in (
        "locations",
        "cdn_site_roles",
        "cdnsites",
        "failover_site",
        "tags",
    ):
        if os.path.isdir(os.path.join(repository_record.filesystem_path, filter_type)):
            msg = (
                f'Found "{filter_type}" directory in the repository root. If this is meant to contain cdn config contexts, '
                "it should be moved into a `cdn_config_contexts/` subdirectory."
            )
            logger.warning(msg)
            job_result.log(msg, level_choice=LogLevelChoices.LOG_WARNING, grouping="cdn config contexts")

        dir_path = os.path.join(cdn_config_context_path, filter_type)
        if not os.path.isdir(dir_path):
            continue

        for file_name in os.listdir(dir_path):
            name = os.path.splitext(file_name)[0]
            msg = f'Loading config context, filter `{filter_type} = [name: "{name}"]`, from `{filter_type}/{file_name}`'
            logger.info(msg)
            job_result.log(msg, grouping="cdn config contexts")
            try:
                with open(os.path.join(dir_path, file_name), "r") as fd:
                    # Data file can be either JSON or YAML; since YAML is a superset of JSON, we can load it regardless
                    context_data = yaml.safe_load(fd)

                # Unlike the above case, these files always contain just a single config context record

                # Add the implied filter to the context metadata
                if filter_type == "device_types":
                    context_data.setdefault("_metadata", {}).setdefault(filter_type, []).append({"model": name})
                else:
                    context_data.setdefault("_metadata", {}).setdefault(filter_type, []).append({"name": name})

                context_name = import_cdn_config_context(context_data, repository_record, job_result)
                managed_cdn_config_contexts.add(context_name)
            except Exception as exc:
                msg = f"Error in loading config context data from `{file_name}`: {exc}"
                logger.error(msg)
                job_result.log(msg, level_choice=LogLevelChoices.LOG_ERROR, grouping="cdn config contexts")

    # Finally, handle device- and virtual-machine-specific "local" context in (devices|virtual_machines)/<name>.(json|yaml)
    for local_type in ("devices", "virtual_machines"):
        if os.path.isdir(os.path.join(repository_record.filesystem_path, local_type)):
            msg = (
                f'Found "{local_type}" directory in the repository root. If this is meant to contain cdn config contexts, '
                "it should be moved into a `cdn_config_contexts/` subdirectory."
            )
            logger.warning(msg)
            job_result.log(msg, level_choice=LogLevelChoices.LOG_WARNING, grouping="cdn config contexts")

        dir_path = os.path.join(cdn_config_context_path, local_type)
        if not os.path.isdir(dir_path):
            continue

        for file_name in os.listdir(dir_path):
            cdnsite_name = os.path.splitext(file_name)[0]
            msg = f"Loading local config context for `{cdnsite_name}` from `{local_type}/{file_name}`"
            logger.info(msg)
            job_result.log(msg, grouping="local cdn config contexts")
            try:
                with open(os.path.join(dir_path, file_name), "r") as fd:
                    context_data = yaml.safe_load(fd)

                import_local_cdn_config_context(
                    local_type,
                    cdnsite_name,
                    context_data,
                    repository_record,
                )
                managed_local_cdn_config_contexts[local_type].add(cdnsite_name)
            except Exception as exc:
                msg = f"Error in loading local config context from `{local_type}/{file_name}`: {exc}"
                logger.error(msg)
                job_result.log(msg, level_choice=LogLevelChoices.LOG_ERROR, grouping="local cdn config contexts")

    # Delete any prior contexts that are owned by this repository but were not created/updated above
    delete_git_cdn_config_contexts(
        repository_record,
        job_result,
        preserve=managed_cdn_config_contexts,
        preserve_local=managed_local_cdn_config_contexts,
    )


def import_cdn_config_context(context_data, repository_record, job_result):  # pylint: disable=redefined-outer-name
    """
    Parse a given dictionary of data to create/update a ConfigContext record.

    The dictionary is expected to have a key "_metadata" which defines properties on the ConfigContext record itself
    (name, weight, description, etc.), while all other keys in the dictionary will go into the record's "data" field.

    Note that we don't use extras.api.serializers.ConfigContextSerializer, despite superficial similarities;
    the reason is that the serializer only allows us to identify related objects (Region, Site, DeviceRole, etc.)
    by their database primary keys, whereas here we need to be able to look them up by other values such as slug.
    """
    git_repository_content_type = ContentType.objects.get_for_model(GitRepository)

    context_record = None
    # TODO: check context_data against a schema of some sort?

    if "_metadata" not in context_data:
        raise RuntimeError("data is missing the required `_metadata` key.")
    if "name" not in context_data["_metadata"]:
        raise RuntimeError("data `_metadata` is missing the required `name` key.")

    # Set defaults for optional fields
    context_metadata = context_data["_metadata"]
    context_metadata.setdefault("weight", 1000)
    context_metadata.setdefault("description", "")
    context_metadata.setdefault("is_active", True)

    # Translate relationship queries/filters to lists of related objects
    relations = {}
    for key, model_class in [
        ("locations", Location),
        ("cdn_site_roles", SiteRole),
        ("cdnsites", CdnSite),
        ("failover_site", CdnSite),
        ("tags", Tag),
    ]:
        relations[key] = []
        for object_data in context_metadata.get(key, ()):
            try:
                object_instance = model_class.objects.get(**object_data)
            except model_class.DoesNotExist as exc:
                raise RuntimeError(
                    f"No matching {model_class.__name__} found for {object_data}; unable to create/update "
                    f"context {context_metadata.get('name')}"
                ) from exc
            except model_class.MultipleObjectsReturned as exc:
                raise RuntimeError(
                    f"Multiple {model_class.__name__} found for {object_data}; unable to create/update "
                    f"context {context_metadata.get('name')}"
                ) from exc
            relations[key].append(object_instance)

    with transaction.atomic():
        # FIXME: Normally ObjectChange records are automatically generated every time we save an object,
        # regardless of whether any fields were actually modified.
        # Because a single GitRepository may manage dozens of records, this would result in a lot of noise
        # every time a repository gets resynced.
        # To reduce that noise until the base issue is fixed, we need to explicitly detect object changes:
        created = False
        modified = False
        save_needed = False
        try:
            context_record = CdnConfigContext.objects.get(
                name=context_metadata.get("name"),
                owner_content_type=git_repository_content_type,
                owner_object_id=repository_record.pk,
            )
        except CdnConfigContext.DoesNotExist:
            context_record = CdnConfigContext(
                name=context_metadata.get("name"),
                owner_content_type=git_repository_content_type,
                owner_object_id=repository_record.pk,
            )
            created = True

        for field in ("weight", "description", "is_active"):
            new_value = context_metadata[field]
            if getattr(context_record, field) != new_value:
                setattr(context_record, field, new_value)
                modified = True
                save_needed = True

        data = context_data.copy()
        del data["_metadata"]

        if context_metadata.get("schema"):
            if getattr(context_record.schema, "name", None) != context_metadata["schema"]:
                try:
                    schema = ConfigContextSchema.objects.get(name=context_metadata["schema"])
                    context_record.schema = schema
                    modified = True
                except ConfigContextSchema.DoesNotExist:
                    job_result.log(
                        f"ConfigContextSchema {context_metadata['schema']} does not exist.",
                        obj=context_record,
                        level_choice=LogLevelChoices.LOG_FAILURE,
                        grouping="cdn config contexts",
                        logger=logger,
                    )
        else:
            if context_record.schema is not None:
                context_record.schema = None
                modified = True

        if context_record.data != data:
            context_record.data = data
            modified = True
            save_needed = True

        if created:
            # Save it so that it gets a PK, required before we can set the relations
            context_record.save()
            save_needed = False

        for key, objects in relations.items():
            field = getattr(context_record, key)
            value = list(field.all())
            if value != objects:
                field.set(objects)
                # Calling set() on a ManyToManyField doesn't require a subsequent save() call
                modified = True

        if save_needed:
            context_record.save()

    if created:
        msg = "Successfully created cdn config context"
        logger.info(msg)
        job_result.log(msg, obj=context_record, level_choice=LogLevelChoices.LOG_INFO, grouping="cdn config contexts")
    elif modified:
        msg = "Successfully refreshed cdn config context"
        logger.info(msg)
        job_result.log(msg, obj=context_record, level_choice=LogLevelChoices.LOG_INFO, grouping="cdn config contexts")
    else:
        msg = "No change to cdn config context"
        logger.info(msg)
        job_result.log(msg, obj=context_record, level_choice=LogLevelChoices.LOG_INFO, grouping="cdn config contexts")

    return context_record.name if context_record else None


def import_local_cdn_config_context(local_type, cdnsite_name, context_data, repository_record):
    """
    Create/update the local cdn config context data associated with a cdnsite.
    """
    try:
        if local_type == "cdnsites":
            record = CdnSite.objects.get(name=cdnsite_name)
    except MultipleObjectsReturned:
        # Possible for Device as name is not guaranteed globally unique
        # TODO: come up with a design that accounts for non-unique names, as well as un-named Devices.
        raise RuntimeError("multiple records with the same name found; unable to determine which one to apply to!")
    except ObjectDoesNotExist:
        raise RuntimeError("record not found!")

    if (
        record.local_cdn_config_context_data_owner is not None
        and record.local_cdn_config_context_data_owner != repository_record
    ):
        logger.error(
            "DATA CONFLICT: Local context data is owned by another owner, %s",
            record.local_cdn_config_context_data_owner,
            extra={"object": record, "grouping": "local cdn config contexts"},
        )
        return

    if record.local_cdn_config_context_data == context_data and record.local_cdn_config_context_data_owner == repository_record:
        logger.info("No change to local cdn config context", extra={"object": record, "grouping": "local cdn config contexts"})
        return

    record.local_cdn_config_context_data = context_data
    record.local_cdn_config_context_data_owner = repository_record
    record.clean()
    record.save()
    logger.info(
        "Successfully updated local cdn config context", extra={"object": record, "grouping": "local cdn config contexts"}
    )


def delete_git_cdn_config_contexts(repository_record, job_result, preserve=(), preserve_local=None):
    """Delete config contexts owned by this Git repository that are not in the preserve list (if any)."""
    if not preserve_local:
        preserve_local = defaultdict(set)

    git_repository_content_type = ContentType.objects.get_for_model(GitRepository)
    for context_record in CdnConfigContext.objects.filter(
        owner_content_type=git_repository_content_type,
        owner_object_id=repository_record.pk,
    ):
        if context_record.name not in preserve:
            context_record.delete()
            msg = f"Deleted CDN config context {context_record}"
            logger.warning(msg)
            job_result.log(msg, level_choice=LogLevelChoices.LOG_WARNING, grouping="config contexts")

    for grouping, model in (
        ("devices", CdnSite),
    ):
        for record in model.objects.filter(
            local_context_data_owner_content_type=git_repository_content_type,
            local_context_data_owner_object_id=repository_record.pk,
        ):
            if record.name not in preserve_local[grouping]:
                record.local_context_data = None
                record.local_context_data_owner = None
                record.clean()
                record.save()
                msg = "Deleted local config context"
                logger.warning(msg)
                job_result.log(
                    msg, obj=record, level_choice=LogLevelChoices.LOG_WARNING, grouping="local cdn config contexts"
                )

register_datasource_contents(
    [
        (
            "extras.gitrepository",
            DatasourceContent(
                name="cdn config contexts",
                content_identifier="nautobot_cdn_models.cdnconfigcontext",
                icon="mdi-code-json",
                weight=500,
                callback=refresh_git_cdn_config_contexts,
            ),
        )
    ]
)