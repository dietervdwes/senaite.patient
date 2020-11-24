# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.PATIENT.
#
# SENAITE.PATIENT is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bika.lims.idserver import generateUniqueId
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Widget import TypesWidget
from senaite.patient.config import AUTO_ID_MARKER


class TemporaryIdentifierWidget(TypesWidget):
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

        value = form.get(field.getName())

        # Allow non-required fields
        if not value:
            return None, {}

        # Is this Identifier temporary?
        true_values = ("true", "1", "on", "True", True, 1)
        temporary = value.get("temporary", False) in true_values

        # The ID might need to be auto-generated if temporary?
        autogenerated = value.get("autogenerated", "")
        identifier = value.get("value") or None
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


# Register widgets
registerWidget(TemporaryIdentifierWidget, title="TemporaryIdentifierWidget")
