from datetime import datetime, timezone
from unittest.mock import patch

import responses
from django.core import cache
from django.test import SimpleTestCase, TestCase
from freezegun import freeze_time
from requests.exceptions import HTTPError, RequestException

from cznic_auctions.loader import get_all_auctions, get_auctions_list, get_auctions_total, get_cache_timeout

API_URL = "https://auctions-master.nic.cz/v1/public/auctions/"


@freeze_time("2023-10-30 08:42:00")
class TestAuctionsLoader(TestCase):
    data = {
        "items": [],
        "total": 100,
        "page": 1,
        "size": 10,
        "pages": 10,
    }
    retval = data.copy()
    retval["current_now"] = datetime(2023, 10, 30, 8, 42, tzinfo=timezone.utc)

    def setUp(self) -> None:
        cache.cache.clear()
        return super().setUp()

    def test_total_load_from_api(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=self.data)
            response = get_auctions_total(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        self.assertEqual(response, self.retval)
        self.assertEqual(cache.cache.get("cms_tests.auctions_total.in_auction.size=1.status=in_auction"), self.retval)

    def test_total_api_exception(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            with self.assertRaisesMessage(RequestException, "Failure."):
                get_auctions_total(
                    {
                        "status": "in_auction",
                        "size": 1,
                    }
                )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_total.in_auction.size=1.status=in_auction"), "__LOAD_ERROR__"
        )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_total.in_auction.size=1.status=in_auction.error"), "Failure."
        )

    def test_total_load_from_cache(self):
        cache.cache.set("cms_tests.auctions_total.in_auction.size=1.status=in_auction", self.retval)
        with responses.RequestsMock():
            response = get_auctions_total(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        self.assertEqual(response, self.retval)

    def test_temporarily_unavailable(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=self.data)
            response = get_auctions_total(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        self.assertEqual(response, self.retval)
        self.assertEqual(cache.cache.get("cms_tests.auctions_total.in_auction.size=1.status=in_auction"), self.retval)

    @patch("cznic_auctions.loader.time.sleep")
    def test_temporarily_unavailable_failure(self, time_sleep):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", status=503)
            with self.assertRaisesMessage(HTTPError, "503 Server Error: Service Unavailable"):
                get_auctions_total(
                    {
                        "status": "in_auction",
                        "size": 1,
                    }
                )
        self.assertEqual(time_sleep.call_count, 10)

    def test_list_load_from_api(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=self.data)
            response = get_auctions_list(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        self.assertEqual(response, self.retval)
        self.assertEqual(cache.cache.get("cms_tests.auctions_list.in_auction.size=1.status=in_auction"), self.retval)

    def test_list_api_exception(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            with self.assertRaisesMessage(RequestException, "Failure."):
                get_auctions_list(
                    {
                        "status": "in_auction",
                        "size": 1,
                    }
                )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_list.in_auction.size=1.status=in_auction"), "__LOAD_ERROR__"
        )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_list.in_auction.size=1.status=in_auction.error"), "Failure."
        )

    def test_list_load_from_cache(self):
        cache.cache.set("cms_tests.auctions_list.in_auction.size=1.status=in_auction", self.retval)
        with responses.RequestsMock():
            response = get_auctions_list(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        self.assertEqual(response, self.retval)

    def test_all_load_from_api(self):
        data = self.data.copy()
        data["pages"] = 1
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=data)
            response = get_all_auctions(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        values = data.copy()
        values["current_now"] = datetime(2023, 10, 30, 8, 42, tzinfo=timezone.utc)
        self.assertEqual(response, values)
        self.assertEqual(cache.cache.get("cms_tests.auctions_all.in_auction.size=1.status=in_auction"), values)

    def test_all_api_exception(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            with self.assertRaisesMessage(RequestException, "Failure."):
                get_all_auctions(
                    {
                        "status": "in_auction",
                        "size": 1,
                    }
                )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_all.in_auction.size=1.status=in_auction"), "__LOAD_ERROR__"
        )
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_all.in_auction.size=1.status=in_auction.error"), "Failure."
        )

    def test_all_more_pages_load_from_api(self):
        data = self.data.copy()
        data["pages"] = 2
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=data)
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1&page=2", json={"items": ["OK"]})
            response = get_all_auctions(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        values = data.copy()
        values["current_now"] = datetime(2023, 10, 30, 8, 42, tzinfo=timezone.utc)
        data = values.copy()
        data["items"] = ["OK"]
        self.assertEqual(response, data)
        self.assertEqual(cache.cache.get("cms_tests.auctions_all.in_auction.size=1.status=in_auction"), values)
        self.assertEqual(
            cache.cache.get("cms_tests.auctions_all.in_auction.page=2.size=1.status=in_auction"),
            {"items": ["OK"], "current_now": values["current_now"]},
        )

    def test_all_load_from_cache(self):
        data = self.retval.copy()
        data["pages"] = 2
        cache.cache.set("cms_tests.auctions_all.in_auction.size=1.status=in_auction", data)
        cache.cache.set("cms_tests.auctions_all.in_auction.page=2.size=1.status=in_auction", {"items": ["OK"]})
        with responses.RequestsMock():
            response = get_all_auctions(
                {
                    "status": "in_auction",
                    "size": 1,
                }
            )
        data["items"] = ["OK"]
        self.assertEqual(response, data)

    def test_cache_error(self):
        cache.cache.set("cms_tests.auctions_all.in_auction.size=1.status=in_auction", "__LOAD_ERROR__")
        cache.cache.set("cms_tests.auctions_all.in_auction.size=1.status=in_auction.error", "Out of order.")
        with responses.RequestsMock():
            with self.assertRaisesMessage(RequestException, "Out of order."):
                get_all_auctions(
                    {
                        "status": "in_auction",
                        "size": 1,
                    }
                )


class TestGetCacheTimeout(SimpleTestCase):
    def test_status_new(self):
        self.assertEqual(get_cache_timeout("new", datetime(2024, 4, 25, 10, 30)), 15)

    def test_status_new_21_00(self):
        self.assertEqual(get_cache_timeout("new", datetime(2024, 4, 25, 21, 0)), 15)

    def test_status_new_21_10(self):
        self.assertEqual(get_cache_timeout("new", datetime(2024, 4, 25, 21, 10)), 15)

    def test_status_new_21_20(self):
        self.assertEqual(get_cache_timeout("new", datetime(2024, 4, 25, 21, 20)), 15)

    def test_status_in_auction(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 10, 30)), 15)

    def test_status_in_auction_20_45(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 45)), 15)

    def test_status_in_auction_20_50(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 50)), 15)

    def test_status_in_auction_20_51(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 51)), 14)

    def test_status_in_auction_20_52(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 52)), 13)

    def test_status_in_auction_20_53(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 53)), 12)

    def test_status_in_auction_20_54(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 54)), 11)

    def test_status_in_auction_20_55(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 55)), 10)

    def test_status_in_auction_20_56(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 56)), 9)

    def test_status_in_auction_20_57(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 57)), 8)

    def test_status_in_auction_20_58(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 58)), 7)

    def test_status_in_auction_20_59(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 20, 59)), 6)

    def test_status_in_auction_21_00(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 21, 0)), 5)

    def test_status_in_auction_21_01(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 21, 1)), 5)

    def test_status_in_auction_21_10(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 21, 10)), 5)

    def test_status_in_auction_21_20(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 21, 20)), 5)

    def test_status_in_auction_21_21(self):
        self.assertEqual(get_cache_timeout("in_auction", datetime(2024, 4, 25, 21, 21)), 15)
