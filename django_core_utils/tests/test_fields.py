"""
.. module::  django_core_utils.tests.test_fields
   :synopsis:  django_core_utils fields unit test module.

*django_core_utils* fields unit test module.
"""
from __future__ import absolute_import, print_function

from inspect import getargspec, getmembers, isfunction

from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

from .. import fields


def _is_no_args(fn):
    """Check if function has no arguments.
    """
    return getargspec(fn).args == []

_field_create_functions = [fn[1] for fn in getmembers(fields)
                           if isfunction(fn[1])]
_no_args_functions = list(filter(_is_no_args, _field_create_functions))


class FieldTestCase(TestCase):
    """Field unitest base class.
    """
    def _assert_create(self, fn, *args, **kwargs):
        """Create a field instance.
        """
        field = fn(*args, **kwargs)
        self.assertTrue(field, 'Field creation error in %s' % fn.__name__)

        return field


class NoArgsFieldsCreateTestCase(FieldTestCase):
    """Check no args field create functions.
    """
    def test_create_no_args(self):
        for fn in _no_args_functions:
            if fn.__name__.endswith('_field'):
                self._assert_create(fn)


class CharFieldTestCase(FieldTestCase):
    """
    Char field unit test class.
    """
    def test_char_field_create(self):
        blank = True
        null = True
        unique = True
        max_length = 10
        field = self._assert_create(fields.char_field,
                                    blank=blank,
                                    null=null,
                                    unique=unique,
                                    max_length=max_length)
        self.assertEqual(field.blank, blank)
        self.assertEqual(field.null, null)
        self.assertEqual(field.unique, unique)
        self.assertEqual(field.max_length, max_length)


class FileFieldTestCase(FieldTestCase):
    """
    File field unit test class.
    """
    def test_file_field_create(self):
        upload_to = "dummy"
        field = self._assert_create(fields.file_field, upload_to=upload_to)
        self.assertEqual(field.upload_to, upload_to)


class DecimalFieldTestCase(FieldTestCase):
    """
    Decimal field unit test class.
    """
    def test_decimal_field_create(self):
        decimal_places = 5
        max_digits = 10
        field = self._assert_create(fields.decimal_field,
                                    decimal_places=decimal_places,
                                    max_digits=max_digits)
        self.assertEqual(field.max_digits, max_digits)
        self.assertEqual(field.decimal_places, decimal_places)


class MyModel(models.Model):
    """Model test class."""
    class Meta(object):
        """Model meta class."""
        app_label = 'test_fields'


class ForeignKeyFieldTestCase(FieldTestCase):
    """
    Foreign key  field unit test class.
    """
    def test_foreign_key_field_create(self):
        field = self._assert_create(fields.foreign_key_field,
                                    to_class=MyModel)

        self.assertEqual(field.related_model.__name__, MyModel.__name__)


class ManyToManyFieldTestCase(FieldTestCase):
    """
    Many to many key  field unit test class.
    """
    def test_many_to_many_field_create(self):
        field = self._assert_create(fields.many_to_many_field,
                                    to_class=MyModel, db_table='dummy')

        self.assertEqual(field.related_model.__name__, MyModel.__name__)


class OneToOneFieldTestCase(FieldTestCase):
    """
    One to One key  field unit test class.
    """
    def test_one_to_one_field_create(self):
        field = self._assert_create(fields.one_to_one_field,
                                    to_class=MyModel)

        self.assertEqual(field.related_model.__name__, MyModel.__name__)


class GeoValidationTestCase(TestCase):
    """Geo location validation test class.
    """

    def test_latitude_validation(self):
        latitude_valid = 0.0
        latitude_invalid_ = 90.05
        value = fields.latitude_validator(latitude_valid)
        self.assertAlmostEqual(value, latitude_valid,
                               "latitude validation error %s" % value)
        self.assertRaises(ValidationError,
                          fields.latitude_validator, latitude_invalid_)

    def test_longitude_validation(self):
        longitude_valid = 0.0
        longitude_invalid = 180.05
        value = fields.longitude_validator(longitude_valid)
        self.assertAlmostEqual(value, longitude_valid,
                               "longitude validation error %s" % value)
        self.assertRaises(ValidationError,
                          fields.longitude_validator, longitude_invalid)
