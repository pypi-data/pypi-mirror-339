# DjangoCMS CZ.NIC Auctions

A group of [Django CMS](https://www.django-cms.org/) plugins for displaying a table with a list of domains in an auction.
The data source is set in the website administration in the [Constance config](https://django-constance.readthedocs.io/en/latest/) section.
The default value is https://auctions-master.nic.cz/v1/public/auctions/.

### Install

`pip install djangocms-cznic-auctions`


Add into settings.py:

```python
INSTALLED_APPS = [
    "constance",
    "cznic_auctions",
    ...
]

AUCTIONS_CONFIG = (
    ("AUCTIONS_LIST_URL", ("https://auctions-master.nic.cz/v1/public/auctions/", "Auctions list URL.", str)),
    ("AUCTIONS_NOT_VERIFY_CERTIFICATE", (False, "Do not verify certificate.", bool)),
)

CONSTANCE_CONFIG = OrderedDict(
    AUCTIONS_CONFIG,
)
CONSTANCE_CONFIG_FIELDSETS = {
    "CZ.NIC Auctions": dict(AUCTIONS_CONFIG).keys(),
}
```

Add into urls.py:

```python
urlpatterns = i18n_patterns(
    ...
    path("auctions/", include(("cznic_auctions.urls", "auctions"), namespace="auctions")),
)
```

### Custom templates

You can define your own template for the domain list.

Add into settings.py:

```python
from cznic_auctions.constants import LIST_TEMPLATES

CZNIC_AUCTIONS_TEMPLATES = LIST_TEMPLATES + [
    ("my-awesome-template/list.html", "My awesome template"),
]
```

## Site example

Along with the program, an example is stored in the repository that you can run in the docker.

Download the example:

```
curl https://gitlab.nic.cz/djangocms-apps/djangocms-cznic-auctions/-/archive/main/djangocms-cznic-auctions-main.zip?path=example --output example.zip
```

Extract the archive and go to the folder:

```
unzip example.zip
cd djangocms-cznic-auctions-main-example/example/
```

Build the image:

```
docker build -t auctions .
```

Run the site:

```
docker run --rm -d -p 8000:8000 --name auctions_example auctions
```

Open the site in your browser: http://localhost:8000/. You'll see what's in the screenshots.

Login to the administration: http://localhost:8000/admin with username `admin` and password `admin`.

Stop the site:

```
docker stop auctions_example
```

![Auctions example](https://gitlab.nic.cz/djangocms-apps/djangocms-cznic-auctions/-/raw/main/screenshots/cznic-auctions.png "Auctions example")

### License

BSD License
