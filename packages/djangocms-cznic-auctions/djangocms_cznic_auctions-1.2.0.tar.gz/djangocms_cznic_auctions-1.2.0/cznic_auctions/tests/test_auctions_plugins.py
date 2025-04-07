import re
import zoneinfo
from collections import OrderedDict, defaultdict
from datetime import datetime, timezone
from typing import Any

import responses
from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from django.contrib.auth.models import AnonymousUser
from django.core import cache
from django.test import TestCase, override_settings, tag
from django.test.client import RequestFactory
from freezegun import freeze_time
from requests.exceptions import RequestException
from sekizai.data import UniqueSequence

from cznic_auctions.cms_plugins import (
    CznicAuctionsExportCSVLinkPlugin,
    CznicAuctionsListPlugin,
    CznicAuctionsTotalPlugin,
)

API_URL = "https://auctions-master.nic.cz/v1/public/auctions/"


class TestsMixin:
    """Data and shared functions mixin."""

    _item = {
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
    }
    _data: dict[str, Any] = {  # type: ignore[misc]
        "total": 42,
        "page": 1,
        "size": 10,
        "pages": 1,
    }
    params = OrderedDict(
        {
            "status": "in_auction",
            "size": 100,
            "page": 1,
            "sort": "price_desc",
        }
    )

    def _get_request(self):
        request = RequestFactory().request()
        request.user = AnonymousUser()
        return request

    def get_data(self):
        data = self._data.copy()
        data["items"] = [self._item]
        return data

    def get_retval(self):
        data = self.get_data()
        data["current_now"] = datetime(2023, 10, 30, 8, 42, tzinfo=timezone.utc)
        return data

    def get_localized_retval(self):
        item = self._item.copy()
        item["auction_from"] = datetime(2023, 10, 23, 17, 43, 7, 460098, tzinfo=zoneinfo.ZoneInfo(key="Europe/Prague"))
        item["auction_to"] = datetime(2023, 11, 3, 16, 43, 7, 460098, tzinfo=zoneinfo.ZoneInfo(key="Europe/Prague"))
        retval = self.get_retval()
        retval["items"][0] = item
        return retval


@freeze_time("2023-10-30 08:42:00")
@tag("ui")
@override_settings(LANGUAGE_CODE="en")
class TestAuctionsTotalPlugin(TestsMixin, TestCase):
    """Test Auctions Total Plugins."""

    def setUp(self) -> None:
        cache.cache.clear()
        return super().setUp()

    def test_context_from_api(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=self.get_data())
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions_total"], self.get_retval())

    def test_context_from_cache(self):
        cache.cache.set("cms_tests.auctions_total.in_auction.size=1.status=in_auction", self.get_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock():
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions_total"], self.get_retval())

    def test_context_api_exception(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertIsNone(context.get("auctions_total"))
        self.assertIsNone(context.get("auctions_total_error"))

    def test_context_api_exception_for_staff(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertIsNone(context.get("auctions_total"))
        self.assertEqual(str(context["auctions_total_error"]), str(RequestException("Failure.")))

    def test_html_from_api(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", json=self.get_data())
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(
            """
            <span class="auctions-total in_auction" title="In auction. Data as of 10/30/2023 9:42 a.m..">42</span>
        """,
            html,
        )

    def test_html_from_cache(self):
        cache.cache.set("cms_tests.auctions_total.in_auction.size=1.status=in_auction", self.get_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        with responses.RequestsMock():
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(
            """
            <span class="auctions-total in_auction" title="In auction. Data as of 10/30/2023 9:42 a.m..">42</span>
        """,
            html,
        )

    def test_html_api_exception(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <span class="auctions-total in_auction data-not-available" title="Data not currently available.">?</span>
        """,
            html,
        )

    def test_html_api_exception_for_staff(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsTotalPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=1", body=RequestException("Failure."))
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <span class="auctions-total in_auction data-not-available"
                title="Data not currently available. Failure.">?</span>
        """,
            html,
        )


@freeze_time("2023-10-30 08:42:00")
@tag("ui")
@override_settings(LANGUAGE_CODE="en")
class TestAuctionsListPlugin(TestsMixin, TestCase):
    """Test Auctions List Plugins."""

    plugin_html = """
        <div class="auctions auctions-list-default">
            <table class="auctions-list in_auction">
                <thead>
                    <tr>
                        <th>Domain</th>
                        <th>Chars</th>
                        <th>Bids</th>
                        <th>Price</th>
                        <th>End of auction</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <a href="https://www.domenovyprohlizec.cz/" target="_blank"
                                title="Go to Domain browser.">synth-07d5d.cz</a>
                        </td>
                        <td>14</td>
                        <td>2</td>
                        <td>300 CZK</td>
                        <td>11/03/2023 4:43 p.m.</td>
                        <td>
                            <img src="/static/cznic_auctions/img/unwatch.svg" width="25" height="25" alt="Unwatch icon"
                                title="Unwatched.">
                            <a class="btn btn-primary" href="https://www.domenovyprohlizec.cz/" target="_blank"
                                title="Go to Domain browser.">Bid</a>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="data-stamp">
                Data as of 10/30/2023 9:42 a.m..
            </div>
        </div>"""

    def setUp(self) -> None:
        cache.cache.clear()
        return super().setUp()

    def test_context_from_api(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", json=self.get_data())
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions"], self.get_localized_retval())

    def test_context_sort_by(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder, CznicAuctionsListPlugin, "en", status="in_auction", sort_by="attractiveness_desc"
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=attractiveness_desc", json=self.get_data()
            )
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions"], self.get_localized_retval())

    def test_context_from_cache(self):
        cache_key = "cms_tests.auctions_list.in_auction.size=10.sort=price_desc.status=in_auction"
        cache.cache.set(cache_key, self.get_localized_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock():
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions"], self.get_localized_retval())
        self.assertTrue(context["show_bid_button"])

    def test_context_no_bid_button(self):
        cache_key = "cms_tests.auctions_list.new.size=10.sort=num_chars_asc.status=new"
        cache.cache.set(cache_key, self.get_localized_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="new")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock():
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertEqual(context["auctions"], self.get_localized_retval())
        self.assertIsNone(context.get("show_bid_button"))

    def test_context_api_exception(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", body=RequestException("Failure.")
            )
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertIsNone(context.get("auctions"))
        self.assertIsNone(context.get("auctions_list_error"))

    def test_context_api_exception_for_staff(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        plugin_instance = model_instance.get_plugin_class_instance()
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", body=RequestException("Failure.")
            )
            context = plugin_instance.render({"request": request}, model_instance, None)
        self.assertIsNone(context.get("auctions"))
        self.assertEqual(str(context["auctions_list_error"]), str(RequestException("Failure.")))

    def test_html_from_api(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", json=self.get_data())
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(self.plugin_html, re.sub(r"unwatch.\w+.svg", "unwatch.svg", html))

    def test_html_from_cache(self):
        cache_key = "cms_tests.auctions_list.in_auction.size=10.sort=price_desc.status=in_auction"
        cache.cache.set(cache_key, self.get_localized_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        with responses.RequestsMock():
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(self.plugin_html, re.sub(r"unwatch.\w+.svg", "unwatch.svg", html))

    def _get_instance_and_renderer(self, status):
        sort = "price_desc" if status == "in_auction" else "num_chars_asc"
        cache_key = f"cms_tests.auctions_list.{status}.size=10.sort={sort}.status={status}"
        cache.cache.set(cache_key, self.get_localized_retval())
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status=status)
        renderer = ContentRenderer(request=RequestFactory())
        return model_instance, renderer

    def _render_auctions_list(self, status):
        model_instance, renderer = self._get_instance_and_renderer(status)
        with responses.RequestsMock():
            return renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})

    def test_html_no_button_bid_in_auction(self):
        html = self._render_auctions_list("in_auction")
        self.assertInHTML(
            """
            <div class="auctions auctions-list-default">
                <table class="auctions-list in_auction">
                    <thead>
                        <tr>
                            <th>Domain</th>
                            <th>Chars</th>
                            <th>Bids</th>
                            <th>Price</th>
                            <th>End of auction</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <a href="https://www.domenovyprohlizec.cz/" target="_blank"
                                    title="Go to Domain browser.">synth-07d5d.cz</a>
                            </td>
                            <td>14</td>
                            <td>2</td>
                            <td>300 CZK</td>
                            <td>11/03/2023 4:43 p.m.</td>
                            <td>
                                <img src="/static/cznic_auctions/img/unwatch.svg" width="25" height="25"
                                    alt="Unwatch icon" title="Unwatched.">
                                <a class="btn btn-primary" href="https://www.domenovyprohlizec.cz/" target="_blank"
                                    title="Go to Domain browser.">Bid</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
                    <div class="data-stamp">Data as of 10/30/2023 9:42 a.m..</div>
            </div>""",
            re.sub(r"unwatch.\w+.svg", "unwatch.svg", html),
        )

    def test_html_no_button_bid_new(self):
        model_instance, renderer = self._get_instance_and_renderer("new")
        with responses.RequestsMock():
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(
            """
            <div class="auctions auctions-list-default">
                <table class="auctions-list new">
                    <thead>
                        <tr>
                            <th>Domain</th>
                            <th>Chars</th>
                            <th>Bids</th>
                            <th>Price</th>
                            <th>Start date</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <a href="https://www.domenovyprohlizec.cz/" target="_blank"
                                    title="Go to Domain browser.">synth-07d5d.cz</a>
                            </td>
                            <td>14</td>
                            <td>2</td>
                            <td>300 CZK</td>
                            <td>10/23/2023 5:43 p.m.</td>
                            <td>
                                <img src="/static/cznic_auctions/img/unwatch.svg" width="25" height="25"
                                    alt="Unwatch icon" title="Unwatched.">
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="data-stamp">
                    Data as of 10/30/2023 9:42 a.m..
                </div>
            </div>""",
            re.sub(r"unwatch.\w+.svg", "unwatch.svg", html),
        )

    def test_html_api_exception(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", body=RequestException("Failure.")
            )
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <div class="auctions auctions-list-default">
                <table class="auctions-list in_auction">
                    <thead>
                        <tr>
                            <th>Domain</th>
                            <th>Chars</th>
                            <th>Bids</th>
                            <th>Price</th>
                            <th>End of auction</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td colspan="6">
                                <div class="data-not-available">Data not currently available.</div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>""",
            html,
        )

    def test_html_api_exception_for_staff(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsListPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", body=RequestException("Failure.")
            )
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <div class="auctions auctions-list-default">
                <table class="auctions-list in_auction">
                    <thead>
                        <tr>
                            <th>Domain</th>
                            <th>Chars</th>
                            <th>Bids</th>
                            <th>Price</th>
                            <th>End of auction</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td colspan="6">
                                <div class="data-not-available">Data not currently available.</div>
                                <ul class="messagelist">
                                    <li class="error">Failure.</li>
                                </ul>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>""",
            html,
        )

    def test_template_list_bids_price_failure(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            CznicAuctionsListPlugin,
            "en",
            status="in_auction",
            template="cznic_auctions/list_bids_price.html",
        )
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", body=RequestException("Failure.")
            )
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <div class="auctions auctions-list-bids-prices">
                <div class="auctions-list in_auction">
                    <div class="row">
                        <div class="data-not-available">Data not currently available.</div>
                            <ul class="messagelist">
                                <li class="error">Failure.</li>
                            </ul>
                    </div>
                </div>
            </div>""",
            html,
        )

    def test_template_list_bids_price(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            CznicAuctionsListPlugin,
            "en",
            status="in_auction",
            template="cznic_auctions/list_bids_price.html",
        )
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", json=self.get_data())
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <div class="auctions auctions-list-bids-prices">
                <div class="auctions-list in_auction">
                    <div class="row">
                        <div><span>1</span></div>
                        <div>
                            <a href="https://www.domenovyprohlizec.cz/" target="_blank"
                                title="Go to Domain browser.">synth-07d5d.cz</a>
                        </div>
                        <div><span>2</span></div>
                        <div><span>300 CZK</span></div>
                    </div>
                </div>
                <div class="data-stamp">
                    Data as of 10/30/2023 9:42 a.m..
                </div>
            </div>""",
            html,
        )

    @override_settings(CZNIC_AUCTIONS_TEMPLATES=[("custom_list.html", "List")])
    def test_custom_template(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder, CznicAuctionsListPlugin, "en", status="in_auction", template="custom_list.html"
        )
        renderer = ContentRenderer(request=RequestFactory())
        request = self._get_request()
        request.user.is_staff = True
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f"{API_URL}?status=in_auction&size=10&sort=price_desc", json=self.get_data())
            html = renderer.render_plugin(
                model_instance,
                {
                    "SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence),
                    "request": request,
                },
            )
        self.assertInHTML(
            """
            <div>
                <div>synth-07d5d.cz</div>
                <div>2</div>
                <div>300</div>
            </div>""",
            html,
        )


@override_settings(LANGUAGE_CODE="en")
class TestAuctionsExportCsvLinkPlugin(TestCase):
    """Test Auctions Export to CSV link Plugins."""

    def test_html(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, CznicAuctionsExportCSVLinkPlugin, "en", status="in_auction")
        renderer = ContentRenderer(request=RequestFactory())
        with responses.RequestsMock():
            html = renderer.render_plugin(model_instance, {"SEKIZAI_CONTENT_HOLDER": defaultdict(UniqueSequence)})
        self.assertInHTML(
            """
            <a class="auctions-export in_auction"
                href="/auctions/export-csv/in_auction/">Export the whole list to csv</a>""",
            html,
        )
