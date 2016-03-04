"""
.. module::  core.models_organization
   :synopsis:  django-utils core demographics models module

django-utils core organization models module.

"""

from core.models import app_table_name, db_table_name

from .models import NamedObject

_app_label = 'core'


class Title(NamedObject):
    """Title model class.

    Capture title/position attributes.
    Sample values may include "Research Analyst", "unknown"
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Title"))


class Role(NamedObject):
    """Role model class.

    Capture role attributes.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Role"))
