"""
.. module::  core.tests.test_models
   :synopsis: django-utils models unit test module.

*django-utils* models unit test module.  The unit tests for
 abstract models are implemented in a separate project due
 to Django not  handling of dynamic model db table creation.
"""
from __future__ import print_function

from ..models import VersionedModel

from django.test import TestCase

from ..models import verbose_class_name, pluralize, db_table_for_class
from ..models import db_table_for_app_and_class, db_table

_app_label = 'test_inflection'


class MyModel(VersionedModel):
    class Meta(VersionedModel.Meta):
        app_label = _app_label


class InflectionTestCase(TestCase):
    """Inflection usage  unitest  class.
    """
    expected_table_name = "sl_test_inflection_my_model"

    def test_verbose_class_name(self):
        verbose_name = verbose_class_name(MyModel.__name__)
        self.assertEqual(verbose_name, "my model",
                         "verbose class name error %s" % verbose_name)

    def test_pluralize(self):
        pluralized = pluralize(MyModel.__name__)
        self.assertEqual(pluralized, "MyModels",
                         "pluralized error %s" % pluralized)

    def test_db_table_for_class(self):
        name = db_table_for_class(MyModel.__name__)
        self.assertEqual(name, "my_model",
                         "db_table_for_class error %s" % name)

    def test_db_table_for_app_and_class(self):
        name = db_table_for_app_and_class(
            _app_label,
            db_table_for_class(MyModel.__name__),
            site_label=None)
        self.assertEqual(name, self.expected_table_name,
                         "db_table_name error %s" % name)

    def test_db_table(self):
        name = db_table(
            _app_label,
            db_table_for_class(MyModel.__name__),
            site_label=None)
        self.assertEqual(name, self.expected_table_name,
                         "db_table_name error %s" % name)
