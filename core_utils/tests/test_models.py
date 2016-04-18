"""
.. module::  core.tests.test_models
   :synopsis: django-utils models unit test module.

*django-utils* models unit test module.  The unit tests for
 abstract models are implemented in a separate project due
 to Django not  handling of dynamic model db table creation.
"""
from __future__ import absolute_import, print_function

from django.test import TestCase

from ..models import (NamedModel, VersionedModel, db_table,
                      db_table_for_app_and_class, db_table_for_class,
                      pluralize, verbose_class_name)

_app_label = 'test_inflection'


class MyModel(VersionedModel):
    """Sample model class."""
    class Meta(VersionedModel.Meta):
        """Meta model class."""
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


class VersionedModelTestCase(TestCase):
    """Versioned model   unitest  class.
    """
    def test_str(self):
        expected = 'MyModel object None'
        instance = MyModel()
        self.assertTrue(str(instance).startswith(expected))


class MyNamedModel(NamedModel):
    """Sample named model class."""
    class Meta(NamedModel.Meta):
        """Meta model class."""
        app_label = _app_label


class NamedModelTestCase(TestCase):
    """Named model   unitest  class.
    """
    def test_str(self):
        myname = 'myname'
        instance = MyNamedModel(name=myname)
        self.assertEqual(str(instance), myname, "invalid str result")
