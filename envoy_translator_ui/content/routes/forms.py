
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from envoy_translator_ui.api import envoy_translator



# class CreateRouteForm(forms.SelfHandlingForm):
#     route_name = forms.CharField(max_length=255, required=True, label=_("Route Name"))
#     description = forms.CharField(required=True, label=_("Description"))
#     ip = forms.GenericIPAddressField(required=True, label=_("Route Attach IP"))
#     port = forms.IntegerField(required=True, label=_("Route Attach Port"), min_value=1, max_value=65535)
#     external_ip = forms.GenericIPAddressField(required=True, label=_("External IP"))
#     type = forms.ChoiceField(label=_("Route Type"),
#                              required=True,
#                              initial="tls",
#                              choices=(("http", _("HTTP")), ("tls", _("TLS")), ("TCP", _("TCP"))))
#     def handle(self, request, data):
#         try:
#             response = envoy_translator.route_create(request, data)
#             if response.status_code == 200:
#                 messages.success(request, _('Created route successfully.'))
#             else:
#                 messages.error(request, _('Failed to create route.'))
#             return True
#         except Exception:
#             messages.error(request, _('Failed to create route.'))
#             return False

