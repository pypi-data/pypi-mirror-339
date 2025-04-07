import csv
from typing import Any

import requests
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from .constants import STATUS_CHOICES, StatusType
from .loader import get_all_auctions


class AuctionsExportCsv(View):
    """Auctions export to CSV."""

    def get(self, request: HttpRequest, status: str, *args: Any, **kwargs: Any) -> HttpResponse:
        if status not in [code for code, _ in STATUS_CHOICES]:
            raise Http404("Unknown status.")
        params = {
            "status": status,
            "size": 100,
            "page": 1,
            "sort": "auction_from_desc",
        }
        try:
            auctions = get_all_auctions(params)
        except requests.RequestException as error:
            raise Http404(error) from error
        response = HttpResponse(content_type="text/csv", charset="utf-8")
        response["Content-Disposition"] = "attachment; filename=auctions_{}_{}.csv".format(
            status, (auctions["current_now"].isoformat()).replace(" ", "_")
        )
        writer = csv.writer(response)
        if status == StatusType.new.value:
            field_label, field_key = _("Start date"), "auction_from"
        else:
            field_label, field_key = _("End of auction"), "auction_to"
        columns = (
            _("Domain"),
            _("Chars"),
            _("Bids"),
            _("Price"),
            field_label + " (UTC)",
        )
        writer.writerow(map(force_str, columns))
        for line in auctions["items"]:
            data = (
                line["item_title"],
                line["num_chars"],
                line["num_bids"],
                line["current_price"],
                line[field_key],
            )
            writer.writerow(["" if column is None else force_str(column) for column in data])
        return response
