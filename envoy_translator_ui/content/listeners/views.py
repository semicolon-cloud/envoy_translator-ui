# Copyright (c) 2016 Catalyst IT Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from horizon import forms
from horizon import tables as horizon_tables
from horizon.utils import memoized
from envoy_translator_ui.content.listeners import tabs as listener_tabs

from envoy_translator_ui.api import envoy_translator
from envoy_translator_ui.content.listeners import forms as listener_forms
from envoy_translator_ui.content.listeners import tables


class IndexView(horizon_tables.DataTableView):
    page_title = _("External Listeners")
    table_class = tables.ExternalListenersTable
    template_name = 'project/listeners/index.html'

    def get_data(self):
        try:
            return envoy_translator.listener_list(self.request)
        except Exception:
            exceptions.handle(self.request, _('Failed to list quota sizes.'))
            return []

class ListenerDetailView(tabs.TabView):
    tab_group_class = listener_tabs.ListenerDetailTabs
    template_name = 'horizon/common/_detail.html'
    redirect_url = 'horizon:project:listeners:index'
    page_title = "{{ listener.listener_name }}"

    def get_context_data(self, **kwargs):
        context = super(ListenerDetailView, self).get_context_data(**kwargs)
        listener, routes = self.get_data()

        context["listener"] = listener
        context["routes"] = routes
        context["url"] = reverse(self.redirect_url)
        context["actions"] = self._get_actions(listener=listener)
        return context

    def _get_actions(self, listener):
        table = tables.ExternalListenersTable(self.request)
        return table.render_row_actions(listener)

    @memoized.memoized_method
    def get_data(self):
        obj = envoy_translator.listener_get(self.request, self.kwargs['listener_id'])
        if obj['errors']:
            raise exceptions.NotAuthorized()
        return obj['listener'], obj['routes']


    def get_tabs(self, request, *args, **kwargs):
        listener, routes = self.get_data()
        return self.tab_group_class(request, listener=listener, routes=routes, **kwargs)

class CreateListenerView(forms.ModalFormView):
    form_class = listener_forms.CreateListenerForm
    form_id = "create_listener_form"
    modal_header = _("Create Listener")
    submit_label = _("Create Listener")
    submit_url = reverse_lazy('horizon:project:listeners:create')
    template_name = 'project/listeners/create.html'
    context_object_name = 'project_users'
    success_url = reverse_lazy("horizon:project:listeners:index")
    page_title = _("Create Listener")

