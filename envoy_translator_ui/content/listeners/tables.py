from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon import exceptions


from envoy_translator_ui.api import envoy_translator
class DeleteListener(tables.DeleteAction):
    name = 'Delete Listener'
    def delete(self, request, obj_id):
        result = envoy_translator.listener_delete(request, obj_id)

        if not result or result.status_code not in [200, 202]:
            exception = exceptions.NotAvailable()
            exception._safe_message = False
            raise exception


    def allowed(self, request, listener=None):
        return True


    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Listener",
            u"Delete Listeners",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Listener",
            u"Deleted Listeners",
            count
        )



class CreateListener(tables.LinkAction):
    name = "invite"
    verbose_name = _("Invite User")
    url = "horizon:project:listeners:create"
    classes = ("ajax-modal",)
    icon = "plus"

class ExternalListenersTable(tables.DataTable):
    name = tables.Column("listener_name", verbose_name=_("Name"), link=("horizon:project:listeners:detail"))
    status = tables.Column("external_ip", verbose_name=_("External IP"))
    port = tables.Column("port", verbose_name=_("External Port"))
    type = tables.Column("type", verbose_name=_("Type"))

    class Meta(object):
        name = "listeners"
        verbose_name = _("Listeners")
        table_actions = (CreateListener, )
        row_actions = (DeleteListener, )

    def get_object_id(self, datum):
        """Returns the identifier for the object this row will represent.

        By default this returns an ``id`` attribute on the given object,
        but this can be overridden to return other values.

        .. warning::

            Make sure that the value returned is a unique value for the id
            otherwise rendering issues can occur.
        """
        return datum['uuid']

class ListenerRoutesTable(tables.DataTable):
    uuid = tables.Column("uuid", verbose_name=_("UUID"))
    project_id = tables.Column("project_id", verbose_name="Project")
    keystone_user = tables.Column("keystone_user", verbose_name="Owner")
    domain_names = tables.Column("domain_names", verbose_name="Domain Names")
    target_servers = tables.Column("target_servers", verbose_name="Target Addresses")

    class Meta(object):
        name = "routes"
        verbose_name = _("Routes")

    def get_object_id(self, datum):
        """Returns the identifier for the object this row will represent.

        By default this returns an ``id`` attribute on the given object,
        but this can be overridden to return other values.

        .. warning::

            Make sure that the value returned is a unique value for the id
            otherwise rendering issues can occur.
        """
        return datum['uuid']