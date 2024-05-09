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
    tab_group_class = listener_tabs.TaskDetailTabs
    template_name = 'horizon/common/_detail.html'
    redirect_url = 'horizon:project:listeners:index'
    page_title = "{{ listener.listener_name }}"

    def get_context_data(self, **kwargs):
        context = super(ListenerDetailView, self).get_context_data(**kwargs)
        listener, routes = self.get_data()

        context["listener"] = listener
        context["routes"] = routes
        context["url"] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        obj = envoy_translator.listener_get(self.request, self.kwargs['listener_id'])
        return obj['listener'], obj['routes']


    def get_tabs(self, request, *args, **kwargs):
        task = self.get_data()
        return self.tab_group_class(request, task=task, **kwargs)
