import time
from datetime import datetime
from typing import Any, Callable

import requests
from constance import config
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .constants import StatusType

DataType = dict[str, Any]  # type: ignore[misc]

LOAD_ERROR = "__LOAD_ERROR__"

# From 21:00 to 21:20 it should be every 5 minutes.
RUSH_TIME_FROM, RUSH_TIME_TO = 21 * 60, 21 * 60 + 20


def get_cache_timeout(status: str, current_now: datetime) -> int:
    """Get cache timeout in minutes."""
    timeout = 15  # 15 minutes.
    short_timeout = 5  # 5 minutes.
    if status == StatusType.in_auction.value:
        current_minutes = current_now.hour * 60 + current_now.minute
        current_timeout = current_minutes + timeout
        time_from_short = RUSH_TIME_FROM + short_timeout
        if current_minutes > RUSH_TIME_TO or current_timeout < time_from_short:
            return timeout
        if current_minutes >= RUSH_TIME_FROM:
            return short_timeout
        return timeout - (current_timeout - time_from_short)
    return timeout


def cached_data(cache_name: str) -> Callable[[Callable], Callable]:
    """Cache data decorator."""

    def wrapper(fnc: Callable) -> Callable[[DataType], DataType]:
        def inner(params: DataType) -> DataType:
            """Get data."""
            keep_error_in_cache = 30
            status = params["status"]
            cache_suffix = ".".join(sorted([f"{key}={value}" for key, value in params.items()]))
            cache_key = f"{settings.CMS_CACHE_PREFIX}{cache_name}.{status}.{cache_suffix}"
            cache_key_error = f"{cache_key}.error"
            result = cache.get(cache_key)
            if result is not None:
                if result == LOAD_ERROR:
                    raise requests.RequestException(cache.get(cache_key_error))
                return result
            try:
                data = fnc(params)
            except requests.RequestException as error:
                cache.set(cache_key, LOAD_ERROR, keep_error_in_cache)
                cache.set(cache_key_error, str(error), keep_error_in_cache)
                raise
            data["current_now"] = timezone.now()
            cache.set(cache_key, data, get_cache_timeout(status, data["current_now"]) * 60)
            return data

        return inner

    return wrapper


def _get_response(params: DataType) -> requests.models.Response:
    """Get response."""
    return requests.get(
        config.AUCTIONS_LIST_URL,  # type: ignore[attr-defined]
        params=params,
        timeout=5.0,
        verify=not config.AUCTIONS_NOT_VERIFY_CERTIFICATE,  # type: ignore[attr-defined]
    )


def _load_from_api(params: DataType) -> DataType:
    """Load data from API."""
    response = _get_response(params)
    if response.status_code == 503:
        # Service is temporarily unavailable. Try reloading ten times.
        for _n in range(10):
            time.sleep(1)
            response = _get_response(params)
            if response.ok:
                break
    response.raise_for_status()
    return response.json()


@cached_data("auctions_list")
def get_auctions_list(params: DataType) -> DataType:
    """Get auctions list."""
    data = _load_from_api(params)
    ctz = timezone.get_current_timezone()
    for item in data["items"]:
        auction_from = parse_datetime(item["auction_from"])
        if auction_from is not None:
            auction_from_naive = timezone.make_naive(auction_from)
            item["auction_from"] = timezone.make_aware(auction_from_naive, timezone=ctz)
        auction_to = parse_datetime(item["auction_to"])
        if auction_to is not None:
            auction_to_naive = timezone.make_naive(auction_to)
            item["auction_to"] = timezone.make_aware(auction_to_naive, timezone=ctz)
    return data


@cached_data("auctions_total")
def get_auctions_total(params: DataType) -> DataType:
    """Get auctions total."""
    return _load_from_api(params)


def get_all_auctions(params: DataType) -> DataType:
    """Get auctions all data."""
    response = cached_data("auctions_all")(_load_from_api)(params)
    pages = response["pages"]
    items = response["items"]
    for index in range(pages - 1):
        params["page"] = index + 2
        page = cached_data("auctions_all")(_load_from_api)(params)
        items.extend(page["items"])
    return response
