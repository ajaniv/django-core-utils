"""
.. module::  core.models_location
   :synopsis:  django-utils core location models module

django-utils core location models module.

"""

from core.models import app_table_name, db_table_name
from . import fields
from .models import NamedObject

_app_label = 'core'


class Timezone(NamedObject):
    """
    Time zone model class.

    Captures time zone attributes.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Timezone"))

    time_zone = fields.time_zone_field()


class Language(NamedObject):
    """Language model class.

    Uses 2 characters as per ISO 639-1.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Language"))

    iso_code = fields.char_field(max_length=2)


class Country(NamedObject):
    """Country model class.

    Uses 2 characters as per  ISO 3166.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Country"))

    iso_code = fields.char_field(max_length=2)


class Region(NamedObject):
    """Abstract class for state and province model.

    Uses 3 characters as per ISO 3166.
    """
    class Meta(NamedObject.Meta):
        abstract = True
        app_label = _app_label

    iso_code = fields.char_field(max_length=3)
    country = fields.foreign_key_field(Country)


class State(Region):
    """State model class."""
    class Meta(Region.Meta):
        db_table = app_table_name(_app_label, db_table_name("State"))


class Province(Region):
    """Province model class."""
    class Meta(Region.Meta.Meta):
        db_table = app_table_name(_app_label, db_table_name("Province"))
