from django.test import SimpleTestCase

from cznic_auctions.models import Auctions, AuctionsList


class TestAuctionsList(SimpleTestCase):
    def test(self):
        instance = AuctionsList(status="new")
        self.assertEqual(str(instance), "New 10")

    def test_sort_by(self):
        instance = AuctionsList(status="new", sort_by="auction_from_desc")
        self.assertEqual(str(instance), "New 10 Auctions from (descending)")


class TestAuctions(SimpleTestCase):
    def test(self):
        instance = Auctions(status="in_auction")
        self.assertEqual(str(instance), "In auction")
