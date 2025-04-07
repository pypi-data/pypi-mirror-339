from collections import OrderedDict
from datetime import datetime, timezone
from urllib.parse import urlencode

import responses
from django.core import cache
from django.http import HttpResponseNotFound
from django.test import TestCase, override_settings, tag
from django.urls import reverse
from freezegun import freeze_time
from requests.exceptions import RequestException

API_URL = "https://auctions-master.nic.cz/v1/public/auctions/"


@freeze_time("2023-10-30 08:42:00")
@tag("ui")
@override_settings(LANGUAGE_CODE="en")
class TestAuctionsViews(TestCase):
    """Test Auctions Views."""

    data = {
        "items": [
            {
                "auction_id": "8c94fa90-fa40-4259-b475-c27dcc8b7e92",
                "item_title": "synth-07d5d.cz",
                "item_description": "DESCRIPTION",
                "initial_price": "100",
                "auction_from": "2023-10-23T15:43:07.460098Z",
                "auction_to": "2023-11-03T15:43:07.460098Z",
                "status": "in_auction",
                "current_price": "300",
                "num_bids": 2,
                "num_chars": 14,
            },
        ],
        "total": 1,
        "page": 1,
        "size": 10,
        "pages": 1,
    }
    retval = data.copy()
    retval["current_now"] = datetime(2023, 10, 30, 8, 42, tzinfo=timezone.utc)
    params = OrderedDict(
        {
            "status": "in_auction",
            "size": 100,
            "page": 1,
            "sort": "auction_from_desc",
        }
    )
    cache_key = "cms_tests.auctions_all.in_auction.page=1.size=100.sort=auction_from_desc.status=in_auction"

    def setUp(self) -> None:
        cache.cache.clear()
        return super().setUp()

    def test_load_from_api(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?{urlencode(self.params)}", json=self.data)
            response = self.client.get(reverse("auctions:auctions_export_csv", kwargs={"status": "in_auction"}))
        self.assertEqual(response.get("Content-Type"), "text/csv")
        self.assertEqual(
            response.get("Content-Disposition"),
            "attachment; filename=auctions_in_auction_2023-10-30T08:42:00+00:00.csv",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            "\r\n".join(
                (
                    "Domain,Chars,Bids,Price,End of auction (UTC)",
                    "synth-07d5d.cz,14,2,300,2023-11-03T15:43:07.460098Z",
                    "",
                )
            ),
        )
        self.assertEqual(cache.cache.get(self.cache_key), self.retval)

    def test_status_new(self):
        cache_key = "cms_tests.auctions_all.new.page=1.size=100.sort=auction_from_desc.status=new"
        cache.cache.set(cache_key, self.retval)
        with responses.RequestsMock():
            response = self.client.get(reverse("auctions:auctions_export_csv", kwargs={"status": "new"}))
        self.assertEqual(response.get("Content-Type"), "text/csv")
        self.assertEqual(
            response.get("Content-Disposition"), "attachment; filename=auctions_new_2023-10-30T08:42:00+00:00.csv"
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            "\r\n".join(
                ("Domain,Chars,Bids,Price,Start date (UTC)", "synth-07d5d.cz,14,2,300,2023-10-23T15:43:07.460098Z", "")
            ),
        )

    def _assert_status(self, status):
        cache_key = f"cms_tests.auctions_all.{status}.page=1.size=100.sort=auction_from_desc.status={status}"
        cache.cache.set(cache_key, self.retval)
        with responses.RequestsMock():
            response = self.client.get(reverse("auctions:auctions_export_csv", kwargs={"status": status}))
        self.assertEqual(response.get("Content-Type"), "text/csv")
        self.assertEqual(
            response.get("Content-Disposition"), f"attachment; filename=auctions_{status}_2023-10-30T08:42:00+00:00.csv"
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            "\r\n".join(
                (
                    "Domain,Chars,Bids,Price,End of auction (UTC)",
                    "synth-07d5d.cz,14,2,300,2023-11-03T15:43:07.460098Z",
                    "",
                )
            ),
        )

    def test_status_in_auction(self):
        self._assert_status("in_auction")

    def test_load_from_api_exception(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?{urlencode(self.params)}", body=RequestException("Failure."))
            response = self.client.get(reverse("auctions:auctions_export_csv", kwargs={"status": "in_auction"}))
        self.assertIsInstance(response, HttpResponseNotFound)
        self.assertEqual(cache.cache.get(self.cache_key), "__LOAD_ERROR__")
        self.assertEqual(cache.cache.get(f"{self.cache_key}.error"), "Failure.")

    def test_unknown_status(self):
        with responses.RequestsMock():
            response = self.client.get(reverse("auctions:auctions_export_csv", kwargs={"status": "foo"}))
        self.assertIsInstance(response, HttpResponseNotFound)
        self.assertEqual(cache.cache.get(self.cache_key), None)
        self.assertEqual(cache.cache.get(f"{self.cache_key}.error"), None)
