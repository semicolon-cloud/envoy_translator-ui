from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon import exceptions


from envoy_translator_ui.api import envoy_translator
class DeleteRoute(tables.DeleteAction):
    name = 'Delete Route'
    policy_rules = (('identity', "project_mod_or_admin"),)
    def delete(self, request, obj_id):
        result = envoy_translator.route_delete(request, obj_id)

        if not result or result.status_code not in [200, 202]:
            exception = exceptions.NotAvailable()
            exception._safe_message = False
            raise exception


    def allowed(self, request, route=None):
        return True


    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Route",
            u"Delete Routes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Route",
            u"Deleted Routes",
            count
        )



class CreateRoute(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Route")
    url = "horizon:project:routes:create"
    classes = ("ajax-modal",)
    policy_rules = (('identity', "project_mod_or_admin"),)
    icon = "plus"


class UpdateRoute(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Route")
    url = "horizon:project:routes:update"
    classes = ("ajax-modal",)
    policy_rules = (('identity', "project_mod_or_admin"),)
    icon = "plus"

class ExternalRoutesTable(tables.DataTable):
    id = tables.Column("uuid", verbose_name=_("UUID"), link=("horizon:project:routes:detail"))
    ip = tables.Column("external_ip", verbose_name=_("External IP"))
    port = tables.Column("port", verbose_name=_("External Port"))
    type = tables.Column("type", verbose_name=_("Type"))
    domain_names = tables.Column("domain_names", verbose_name="Domain Names")
    target_servers = tables.Column("target_servers", verbose_name="Target Addresses")

    class Meta(object):
        name = "routes"
        verbose_name = _("Routes")
        table_actions = (CreateRoute, )
        row_actions = (UpdateRoute, DeleteRoute)

    def get_object_id(self, datum):
        """Returns the identifier for the object this row will represent.

        By default this returns an ``id`` attribute on the given object,
        but this can be overridden to return other values.

        .. warning::

            Make sure that the value returned is a unique value for the id
            otherwise rendering issues can occur.
        """
        return datum['uuid']
