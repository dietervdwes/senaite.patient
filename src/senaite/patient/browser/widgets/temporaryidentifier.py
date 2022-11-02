# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bika.lims.idserver import generateUniqueId
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget
from senaite.core.browser.widgets import QuerySelectWidget
from senaite.patient.config import AUTO_ID_MARKER


class TemporaryIdentifierWidget(QuerySelectWidget):
    """A widget for the introduction of temporary IDs (e.g. MRN). It displays
    an input text box for manual introduction of the ID, next to a "Temporary"
    checkbox. When the checkbox is selected, system assumes the ID is temporary
    and must be auto-generated.
    """
    security = ClassSecurityInfo()
    _properties = StringWidget._properties.copy()
    _properties.update({
        "macro": "senaite_patient_widgets/temporaryidentifierwidget",
    })

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):

        fieldname = field.getName()
        identifier = form.get(fieldname)
        # checkboxes are not submitted if not selected!
        temporary = True if form.get(fieldname + "_temporary") else False
        autogenerated = ""

        # Allow non-required fields
        if not identifier:
            return None, {}

        # The ID might need to be auto-generated if temporary?
        if temporary and identifier in [None, AUTO_ID_MARKER]:
            kwargs = {"portal_type": field.getName()}
            identifier = generateUniqueId(api.get_portal(), **kwargs)
            autogenerated = identifier

        value = {
            "temporary": temporary,
            "value": identifier,
            "value_auto": autogenerated,
        }
        return value, {}


registerWidget(TemporaryIdentifierWidget, title="TemporaryIdentifierWidget")
