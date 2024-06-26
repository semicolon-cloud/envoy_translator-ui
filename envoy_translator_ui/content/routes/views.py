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

from horizon import exceptions, views
from horizon import tabs
from horizon import forms
from horizon import tables as horizon_tables
from horizon.utils import memoized

from envoy_translator_ui.api import envoy_translator
from envoy_translator_ui.content.routes import forms as route_forms
from envoy_translator_ui.content.routes import tables


class IndexView(horizon_tables.DataTableView):
    page_title = _("External Routes")
    table_class = tables.ExternalRoutesTable
    template_name = 'project/routes/index.html'

    def get_data(self):
        try:
            return envoy_translator.route_list(self.request)
        except Exception:
            exceptions.handle(self.request, _('Failed to list routes'))
            return []

class RouteDetailView(views.HorizonTemplateView):
    redirect_url = "horizon:project:routes:index"
    template_name = 'project/routes/detail.html'
    page_title = "Route Details: {{ route.uuid }}"

    def get_context_data(self, **kwargs):
        context = super(RouteDetailView, self).get_context_data(
            **kwargs)
        route = self.get_data()
        context["route"] = route
        context["url"] = reverse(self.redirect_url)
        context["actions"] = self._get_actions(route=route)
        return context

    def _get_actions(self, route):
        table = tables.ExternalRoutesTable(self.request)
        return table.render_row_actions(route)

    @memoized.memoized_method
    def get_data(self):
        try:
            route = envoy_translator.route_get(self.request, self.kwargs['route_id'])
            return route
        except Exception:
            msg = _('Unable to retrieve route.')
            url = reverse('horizon:project:routes:index')
            exceptions.handle(self.request, msg, redirect=url)


class CreateRouteView(forms.ModalFormView):
    form_class = route_forms.CreateRouteForm
    form_id = "create_route_form"
    modal_header = _("Create Route")
    submit_label = _("Create Route")
    submit_url = reverse_lazy('horizon:project:routes:create')
    template_name = 'project/routes/create.html'
    context_object_name = 'project_users'
    success_url = reverse_lazy("horizon:project:routes:index")
    page_title = _("Create Route")


class UpdateRouteView(forms.ModalFormView):
    form_class = route_forms.UpdateRouteForm
    form_id = "update_route_form"
    modal_header = _("Update Route")
    submit_label = _("Update")
    submit_url = 'horizon:project:routes:update'
    template_name = 'project/routes/update.html'
    context_object_name = 'project_users'
    success_url = "horizon:project:routes:detail"
    page_title = _("Update Route")

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['route_id'],))

    @memoized.memoized_method
    def get_object(self):
        try:
            return envoy_translator.route_get(self.request,
                                     self.kwargs['route_id'])
        except Exception:
            msg = _('Unable to retrieve route.')
            url = reverse('horizon:management:tasks:index')
            exceptions.handle(self.request, msg, redirect=url)

    def get_context_data(self, **kwargs):
        context = super(UpdateRouteView, self).get_context_data(**kwargs)
        context['route'] = self.get_object()
        args = (self.kwargs['route_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        route = self.get_object()

        data = {
            'route_id': self.kwargs['route_id'],
            'domain_names': '\n'.join(route["domain_names"]),
            'target_servers': '\n'.join([a['ip'] + ":" + a["port"] for a in route["target_servers"]]),
        }
        return data
