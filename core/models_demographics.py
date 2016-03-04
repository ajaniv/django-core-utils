"""
.. module::  core.models_demographics
   :synopsis:  django-utils core demographics models module

django-utils core demographics models module.

"""

from core.models import app_table_name, db_table_name
from . import constants
from .models import NamedObject

_app_label = 'core'
MALE = 'Male'
FEMALE = 'Female'
GENDER = (MALE, FEMALE, constants.UNKNOWN)


class Gender(NamedObject):
    """Gender model class.

    Values make include  "male", "female", "other", "none", "unknown".
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name('Gender'))
