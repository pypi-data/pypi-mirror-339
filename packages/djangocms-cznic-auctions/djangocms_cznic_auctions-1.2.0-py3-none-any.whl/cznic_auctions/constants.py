from enum import Enum, unique

from django.utils.translation import gettext_lazy as _


@unique
class StatusType(Enum):
    """Auctions status."""

    # https://gitlab.office.nic.cz/others/auctions/-/blob/master/auctions/schemas/auction.py#L34-38
    # https://gitlab.office.nic.cz/others/auctions/-/blob/2.1/auctions/views/auction/user_list_view.py?ref_type=heads#L175

    new = "new"
    in_auction = "in_auction"


@unique
class SortType(Enum):
    """Auctions sort type."""

    # https://gitlab.office.nic.cz/others/auctions/-/blob/master/auctions/schemas/auction.py#L100-120

    auction_from_desc = "auction_from_desc"
    num_chars_asc = "num_chars_asc"
    num_chars_desc = "num_chars_desc"
    price_desc = "price_desc"
    price_asc = "price_asc"
    attractiveness_desc = "attractiveness_desc"
    attractiveness_asc = "attractiveness_asc"
    bids_asc = "bids_asc"
    bids_desc = "bids_desc"


STATUS_CHOICES = (
    (StatusType.new.value, _("New")),
    (StatusType.in_auction.value, _("In auction")),
)

SORT_CHOICES = (
    (SortType.auction_from_desc.value, _("Auctions from (descending)")),
    (SortType.num_chars_asc.value, _("Number of characters (ascending)")),
    (SortType.num_chars_desc.value, _("Number of characters (descending)")),
    (SortType.price_desc.value, _("Price (descending)")),
    (SortType.price_asc.value, _("Price (ascending)")),
    (SortType.attractiveness_desc.value, _("Attractiveness (descending)")),
    (SortType.attractiveness_asc.value, _("Attractiveness (ascending)")),
    (SortType.bids_asc.value, _("Bids (ascending)")),
    (SortType.bids_desc.value, _("Bids (descending)")),
)


LIST_TEMPLATES = [
    ("cznic_auctions/list.html", _("Default")),
    ("cznic_auctions/list_bids_price.html", _("Bids, Price")),
]
