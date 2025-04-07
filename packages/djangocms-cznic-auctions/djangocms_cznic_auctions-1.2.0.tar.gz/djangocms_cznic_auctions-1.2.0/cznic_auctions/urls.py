from django.urls import path

from .views import AuctionsExportCsv

urlpatterns = [
    path("export-csv/<slug:status>/", AuctionsExportCsv.as_view(), name="auctions_export_csv"),
]
