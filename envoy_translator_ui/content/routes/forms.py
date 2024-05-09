
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from envoy_translator_ui.api import envoy_translator




def get_listener_choices(request):
    """Get manageable roles for user.

    Returns a list of sorted 2-ary tuples containing the roles the current
    user can manage.
    """
    listeners = envoy_translator.listener_list(request)
    listener_tuples = [(r['uuid'], r['listener_name']) for r in listeners]
    listener_tuples = sorted(listener_tuples, key=lambda listener: listener[1])
    return listener_tuples



class CreateRouteForm(forms.SelfHandlingForm):
    domain_names = forms.CharField(max_length=255, required=True, label=_("list of domains"), widget=forms.widgets.Textarea())
    target_servers = forms.CharField(
        required=True, label=_("List of target servers in ip:port"), widget=forms.widgets.Textarea())
    listener = forms.ChoiceField(label=_("Listener"),
                             required=True)

    def __init__(self, *args, **kwargs):
        super(CreateRouteForm, self).__init__(*args, **kwargs)
        choices = get_listener_choices(self.request)
        self.fields['listener'].choices = choices


    def handle(self, request, data):
        try:
            data["domain_names"] = data["domain_names"].split("\n")
            data["target_servers"] = [ {"ip": a.split(":")[0], "port": a.split(":")[1]} for a in data["target_servers"].split("\n") ]

            response = envoy_translator.route_create(request, data)
            if response.status_code == 200:
                messages.success(request, _('Created route successfully.'))
            else:
                messages.error(request, _('Failed to create route. : %s' % response.text))
            return True
        except Exception:
            messages.error(request, _('Failed to create route.'))
            return False



class UpdateRouteForm(forms.SelfHandlingForm):
    route_id = forms.CharField(widget=forms.HiddenInput())
    domain_names = forms.CharField(max_length=255, required=True, label=_("list of domains"), widget=forms.widgets.Textarea())
    target_servers = forms.CharField(
        required=True, label=_("List of target servers in ip:port"), widget=forms.widgets.Textarea())
    def handle(self, request, data):
        try:
            data["domain_names"] = data["domain_names"].split("\n")
            data["target_servers"] = [ {"ip": a.split(":")[0], "port": a.split(":")[1]} for a in data["target_servers"].split("\n") ]

            response = envoy_translator.route_update(request, data["route_id"], data)
            if response.status_code == 200:
                messages.success(request, _('Updated route successfully.'))
            else:
                messages.error(request, _('Failed to update route. %s ' % response.text))
            return True
        except Exception:
            messages.error(request, _('Failed to create route.'))
            return False

