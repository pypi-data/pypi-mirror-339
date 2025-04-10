"""Models for the CDN app."""
# pylint: disable=duplicate-code, too-many-lines

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.functional import cached_property, classproperty

from nautobot.core.models.generics import OrganizationalModel, PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features, FeatureQuery
from nautobot.core.models.fields import NaturalOrderingField
from nautobot.core.utils.config import get_settings_or_config

from .contexts import CdnConfigContextModel
from ..querysets import CdnConfigContextModelQuerySet


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)

class HyperCacheMemoryProfile(PrimaryModel):
    name = models.CharField(max_length=255, help_text="Profile Name.")
    description = models.CharField(max_length=255, blank=True, help_text="A description of the Memory profile.")
    frontEndCacheMemoryPercent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    ramOnlyCacheMemoryPercent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    hotCacheMemoryPercent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    diskIndexMemoryPercent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    cacheMemoryProfileId = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
    )
    
    csv_headers = ["name", "description", "frontEndCacheMemoryPercent", "ramOnlyCacheMemoryPercent", "hotCacheMemoryPercent", "diskIndexMemoryPercent", "cacheMemoryProfileId"]
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ("name", "description", "frontEndCacheMemoryPercent", "ramOnlyCacheMemoryPercent", "hotCacheMemoryPercent", "diskIndexMemoryPercent", "cacheMemoryProfileId")

@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class SiteRole(OrganizationalModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)


    csv_headers = ["name", "description"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def to_csv(self):
        return (
            self.name,
            self.description,
        )


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)

class CdnSite(PrimaryModel, CdnConfigContextModel):
    name = models.CharField(max_length=255, help_text="Akamai Site Name.")
    _name = NaturalOrderingField(target_field="name", max_length=100, blank=True, db_index=True)
    cdn_site_role = models.ForeignKey(
        to="SiteRole",
        on_delete=models.SET_NULL,
        related_name="cdnsites",
        blank=True,
        null=True,
    )
    status = StatusField(blank=False, null=False)
    location = models.ForeignKey(
        to="dcim.Location",
        on_delete=models.PROTECT,
        related_name="cdnsites",
        blank=True,
        null=True,
    )
    abbreviatedName = models.CharField(max_length=255, blank=True, help_text="Akamai Site Name Abbreviation")
    bandwidthLimitMbps = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(10000000)],
        blank=True,
        null=True,
    )
    enableDisklessMode = models.BooleanField(
        default=False,
        help_text="Enables Diskless Mode for the site, False by default.",
    )
    neighbor1 = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_neighbor",
        help_text="Only required for HPC sites, this defines the primary neighbor"
    )
    neighbor1_preference = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        blank=True,
        null=True,
        default=1000
    )
    neighbor2 = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="secondary_neighbor",
        help_text="Only Required for HPC sites, this defines the secondary neighbor",
    )
    neighbor2_preference = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        blank=True,
        null=True,
        default=750
    )
    failover_site = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sister_site",
        help_text="Select the site to which this site will failover to."
    )
    cacheMemoryProfileId = models.ForeignKey(
        to="HyperCacheMemoryProfile",
        on_delete=models.PROTECT,
        related_name="cdn_sites",
        blank=True,
        null=True,
    )
    siteId = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        blank=True,
        null=True,
        default=None,
    )

    objects = CdnConfigContextModelQuerySet.as_manager()

    csv_headers = [
        "name",
        "status",
        "location",
        "cdn_site_role",
        "abbreviatedName",
        "bandwidthLimitMbps",
        "enableDisklessMode",
        "neighbor1",
        "neighbor1_preference",
        "neighbor2",
        "neighbor2_preference",
        "cacheMemoryProfileId",
        "siteId",

    ]
    clone_fields = [
        "status",
        "location",
        "abbreviatedName",
        "bandwidthLimitMbps",
        "enableDisklessMode",
        "neighbor1",
        "neighbor1_preference",
        "neighbor2",
        "neighbor2_preference",
        "cacheMemoryProfileId",
        "siteId",
    ]

    @classproperty  # https://github.com/PyCQA/pylint-django/issues/240
    def natural_key_field_names(cls):  # pylint: disable=no-self-argument
        """
        When CDN_SITE_NAME_AS_NATURAL_KEY is set in settings or Constance, we use just the `name` for simplicity.
        """
        if get_settings_or_config("CDN_SITE_NAME_AS_NATURAL_KEY"):
            # opt-in simplified "pseudo-natural-key"
            return ["name"]
        else:
            # true natural-key given current uniqueness constraints
            return ["name", "cdn_site_role", "location"]  # location should be last since it's potentially variadic
    class Meta:
        ordering = ["cdn_site_role", "_name"]
        unique_together = (
            ("cdn_site_role", "location", "name"),  # See validate_unique below
        )
    
    def __str__(self):
        return self.name or super().__str__()
       
    def validate_unique(self, exclude=None):
        if self.name and hasattr(self, "cdnsite") and self.location is None:
            if CdnSite.objects.exclude(pk=self.pk).filter(name=self.name, site=self.cdnsite, location__isnull=True):
                raise ValidationError({"name": "A cdnsite with this name already exists."})

        super().validate_unique(exclude)

    def clean(self):
        super().clean()

    
    def to_csv(self):
        return (
            self.name,
            self.cdn_site_role.name if self.cdn_site_role else None,
            self.abbreviatedName,
            self.enableDisklessMode,
            self.bandwidthLimitMbps,
            self.neighbor1,
            self.neighbor1_preference,
            self.neighbor2,
            self.neighbor2_preference,
            self.cacheMemoryProfileId,
            self.status,
            self.location,
            self.siteId,
        )