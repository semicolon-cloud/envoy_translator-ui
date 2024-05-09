import collections
import json
import logging
import requests
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils import functions as utils
from horizon.utils import memoized

from openstack_dashboard.api import base


LOG = logging.getLogger(__name__)


LISTENER = collections.namedtuple('Listener',
                              ['uuid', 'listener_name', 'description',
                               'ip', 'external_ip', 'port', 'type', 'created_on'])

def _get_endpoint_url(request):
    # If the request is made by an anonymous user, this endpoint request fails.
    # Thus, we must hardcode this in Horizon.
    if getattr(request.user, "service_catalog", None):
        url = base.url_for(request, service_type='envoy-translator')


    # Ensure ends in slash
    if not url.endswith('/'):
        url += '/'

    return url



def _request(request, method, url, headers, **kwargs):
    try:
        endpoint_url = _get_endpoint_url(request)
        url = urljoin(endpoint_url, url)
        session = requests.Session()
        data = kwargs.pop("data", None)
        return session.request(method, url, headers=headers,
                               data=data, **kwargs)
    except Exception as e:
        LOG.error(e)
        raise


def head(request, url, **kwargs):
    return _request(request, 'HEAD', url, **kwargs)


def get(request, url, **kwargs):
    return _request(request, 'GET', url, **kwargs)


def post(request, url, **kwargs):
    return _request(request, 'POST', url, **kwargs)


def put(request, url, **kwargs):
    return _request(request, 'PUT', url, **kwargs)


def patch(request, url, **kwargs):
    return _request(request, 'PATCH', url, **kwargs)


def delete(request, url, **kwargs):
    return _request(request, 'DELETE', url, **kwargs)



def listener_list(request):
    try:
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': request.user.token.id}
        resp = json.loads(get(request, 'listeners',
                              headers=headers).content)

        return resp['listeners']
    except Exception as e:
        LOG.error(e)
        raise

