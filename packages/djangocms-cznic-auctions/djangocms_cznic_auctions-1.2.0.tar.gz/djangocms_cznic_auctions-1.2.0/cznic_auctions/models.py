from cms.models.pluginmodel import CMSPlugin
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from .constants import LIST_TEMPLATES, SORT_CHOICES, STATUS_CHOICES


def get_templates() -> list[tuple[str, str]]:
    return getattr(settings, "CZNIC_AUCTIONS_TEMPLATES", LIST_TEMPLATES)


class AuctionsList(CMSPlugin):
    """Auctions list model."""

    status = models.CharField(
        verbose_name=_("Status"), max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[1]
    )
    size = models.PositiveSmallIntegerField(
        verbose_name=_("Table size"),
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        help_text="minimum: 1, maximum: 100",
    )
    sort_by = models.CharField(verbose_name=_("Sort by"), max_length=50, choices=SORT_CHOICES, null=True, blank=True)
    template = models.CharField(
        verbose_name=_("Template"), max_length=255, choices=lazy(get_templates, tuple)(), null=True, blank=True
    )

    def __str__(self):
        sort_by = self.get_sort_by_display()
        if sort_by is None:
            sort_by = ""
        return f"{self.get_status_display()} {self.size} {sort_by}".strip()


class Auctions(CMSPlugin):
    """Auctions model."""

    status = models.CharField(
        verbose_name=_("Status"), max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[1]
    )

    def __str__(self):
        return self.get_status_display()
