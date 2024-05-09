from horizon import tabs

from django.utils.translation import ugettext_lazy as _
from envoy_translator_ui.content.listeners import tables as listener_tables

class ListenerOverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = 'project/listeners/_listener_detail_overview.html'

    def get_context_data(self, request):
        return {"listener": self.tab_group.kwargs['listener'], "routes": self.tab_group.kwargs['routes']}


class ListenerRoutesTab(tabs.TableTab):
    name = _("Routes")
    slug = "routes"
    table_classes = (listener_tables.RoutesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_routes_data(self):
        return self.tab_group.kwargs['routes']


class ListenerDetailTabs(tabs.DetailTabsGroup):
    slug = "listener_details"
    tabs = (ListenerOverviewTab, ListenerRoutesTab)
