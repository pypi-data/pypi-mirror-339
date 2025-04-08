from django.urls import include, path

urlpatterns = [
    path("auctions/", include(("cznic_auctions.urls", "auctions"), namespace="auctions")),
]
