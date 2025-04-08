from collections import OrderedDict

SECRET_KEY = "secret"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sites",
    "cms",
    "constance",
    "menus",
    "treebeard",
    "cznic_auctions",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "tests",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en"
LANGUAGES = (("en", "English"),)

SITE_ID = 1
USE_TZ = True
TIME_ZONE = "Europe/Prague"

ROOT_URLCONF = "cznic_auctions.tests.urls"
CMS_CACHE_PREFIX = "cms_tests."
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

STATIC_URL = "/static/"

AUCTIONS_CONFIG = (  # type: ignore # noqa: F405
    ("AUCTIONS_LIST_URL", ("https://auctions-master.nic.cz/v1/public/auctions/", "Auctions list URL.", "short_str")),
    ("AUCTIONS_NOT_VERIFY_CERTIFICATE", (False, "Do not verify certificate.", bool)),
)
CONSTANCE_CONFIG = OrderedDict(
    AUCTIONS_CONFIG,
)

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["cznic_auctions/templates", "cznic_auctions/tests/templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cms.context_processors.cms_settings",
            ],
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
        },
    }
]
CMS_CONFIRM_VERSION4 = True

CMS_TEMPLATES = (("page.html", "Page"),)
