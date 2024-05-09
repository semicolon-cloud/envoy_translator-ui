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

    def get_object_id(self, datum):
        """Returns the identifier for the object this row will represent.

        By default this returns an ``id`` attribute on the given object,
        but this can be overridden to return other values.

        .. warning::

            Make sure that the value returned is a unique value for the id
            otherwise rendering issues can occur.
        """
        return datum.uuid