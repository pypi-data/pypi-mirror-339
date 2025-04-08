from typing import Any

import requests
from cms.models.placeholdermodel import Placeholder
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .constants import SortType, StatusType
from .loader import get_auctions_list, get_auctions_total
from .models import Auctions, AuctionsList


@plugin_pool.register_plugin
class CznicAuctionsListPlugin(CMSPluginBase):
    """Auctions Plugin."""

    model = AuctionsList
    name = _("CZ.NIC Auctions list")  # type: ignore[assignment]
    module = _("Auctions")
    allow_children = False
    cache = False

    def get_render_template(self, context: dict[str, Any], instance: AuctionsList, placeholder: Placeholder) -> str:
        return "cznic_auctions/list.html" if instance.template is None else instance.template

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        if instance.sort_by is None:
            sort = (
                SortType.price_desc.value
                if instance.status == StatusType.in_auction.value
                else SortType.num_chars_asc.value
            )
        else:
            sort = instance.sort_by
        try:
            context["auctions"] = get_auctions_list(
                {
                    "status": instance.status,
                    "size": instance.size,
                    "sort": sort,
                }
            )
        except requests.RequestException as error:
            if context["request"].user.is_staff:
                context["auctions_list_error"] = error
        if instance.status == StatusType.in_auction.value:
            context["show_bid_button"] = True
        if instance.status == StatusType.new.value:
            context["show_date_from"] = True
        return context


@plugin_pool.register_plugin
class CznicAuctionsTotalPlugin(CMSPluginBase):
    """Total auctions Plugin."""

    model = Auctions
    render_template = "cznic_auctions/total.html"  # type: ignore[assignment]
    name = _("CZ.NIC Auctions total")  # type: ignore[assignment]
    module = _("Auctions")
    allow_children = False
    cache = False
    text_enabled = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        try:
            context["auctions_total"] = get_auctions_total(
                {
                    "status": instance.status,
                    "size": 1,
                }
            )
        except requests.RequestException as error:
            if context["request"].user.is_staff:
                context["auctions_total_error"] = error
        return context


@plugin_pool.register_plugin
class CznicAuctionsExportCSVLinkPlugin(CMSPluginBase):
    """Auctions export CSV link Plugin."""

    model = Auctions
    render_template = "cznic_auctions/export-csv.html"  # type: ignore[assignment]
    name = _("CZ.NIC Auctions Link to export CSV")  # type: ignore[assignment]
    module = _("Auctions")
    allow_children = False
    text_enabled = True
