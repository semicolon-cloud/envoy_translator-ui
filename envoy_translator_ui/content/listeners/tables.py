from django.utils.translation import gettext_lazy as _

from horizon import tables


class ExternalListenersTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    status = tables.Column("external_ip", verbose_name=_("External IP"))
    port = tables.Column("port", verbose_name=_("External Port"))
    type = tables.Column("type", verbose_name=_("Type"))

    class Meta(object):
        name = "listeners"
        verbose_name = _("Listeners")