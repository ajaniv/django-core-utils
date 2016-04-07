"""

..  module:: omcore.utils.tests.test_util.py
    :synopsis: Unit test utilities module

"""
from __future__ import absolute_import, print_function

import os
from random import randrange

import inflection
from django.conf import settings
from django.test import TestCase
from utils.core import instance_class_name

from . import factories
from ..utils import current_site

TEST_DOMAIN = 'ondalear.com'
TEST_USER_NAME = 'test_user'
TEST_USER_PASSWORD = 'pass'
TEST_USER_EMAIL = '{}@{}'.format(TEST_USER_NAME, TEST_DOMAIN)


class TestCaseMixin(object):
    """
    Unit test mixin class.
    """
    def file_path(self, file_name):
        return test_data_file_path(file_name)

    def setUp(self):

        self.username = TEST_USER_NAME
        self.user = factories.UserFactory(username=TEST_USER_NAME)
        self.site = current_site()
        self.saved_debug = settings.DEBUG
        try:
            if settings.FORCE_DEBUG:
                settings.DEBUG = True
        except AttributeError:
            pass

    def tearDown(self):
        settings.DEBUG = self.saved_debug

    def force_debug(self, value=True):
        settings.DEBUG = value


class BaseAppDjangoTestCase(TestCaseMixin, TestCase):
    """Base Django test case class"""
    def setUp(self):
        TestCase.setUp(self)
        TestCaseMixin.setUp(self)

    def tearDown(self):
        TestCaseMixin.tearDown(self)
        TestCase.tearDown(self)


class VersionedModelTestCase(BaseAppDjangoTestCase):
    """Versioned model unit test class.
    """
    def verify_instance(self, instance, version=1, **kwargs):
        self.verify_instances([instance], version, **kwargs)

    def verify_instances(self, instances,
                         count=1, version=1, **kwargs):
        msg = "instance count error; expected:{} allocated:{}"
        self.assertEqual(
            len(instances), count,
            msg.format(count, len(instances)))

        for index, instance in enumerate(instances):
            self.verify_id(index, instance)
            self.verify_get(index, instance)
            self.verify_uuid(index, instance)
            self.verify_timestamps(index, instance)
            self.verify_users(index, instance)
            self.verify_version(index, instance, version)
            self.verify_enabled(index, instance, True)
            self.verify_deleted(index, instance, False)
            self.verify_derived(index, instance)

    def _attribute_msg(self, obj, attribute, index, expected):
        msg = '({}): invalid instance.{}({}) at index({}) expected({})'
        return msg.format(instance_class_name(obj),
                          attribute,
                          getattr(obj, attribute),
                          index, expected)

    def verify_id(self, index, obj):
        """Verify instance id."""
        msg = '({}): invalid instance.{}({}) at index({})'
        self.assertTrue(
            obj.id is not None,
            msg.format(instance_class_name(obj), 'id', obj.id, index))

    def verify_get(self, index, obj):
        """
        Verify instance database fetch using get
        """
        msg = '({}): invalid instance.{}({}) at index({})'
        db_instance = obj.__class__.objects.get_or_none(pk=obj.id)
        self.assertTrue(
            db_instance,
            msg.format(instance_class_name(obj), 'id', obj.id, index))

    def verify_uuid(self, index, obj):
        """Verify instance uuid."""
        msg = '({}): invalid instance.{}({}) at index({})'
        self.assertTrue(
            obj.uuid is not None,
            msg.format(instance_class_name(obj), 'uuid', obj.uuid, index))

    def verify_timestamps(self, index, obj):
        """Verify instance timestamps."""
        msg_set = '({}): invalid instance.{}({}) at index({})'
        msg_value = '{}: time mismatch creation:{} update:{} at index({})'
        for attr in ('creation_time', 'update_time'):
            attr_value = getattr(obj, attr)
            self.assertTrue(
                attr_value,
                msg_set.format(
                    instance_class_name(obj),
                    attr, attr_value, index))
        self.assertTrue(
            obj.creation_time <= obj.update_time,
            msg_value.format(
                instance_class_name(obj),
                obj.creation_time.microsecond,
                obj.update_time.microsecond, index))

    def verify_users(self, index, obj):
        """Verify users."""
        msg = '({}): invalid instance.{}({}) at index({})'
        user_name = self.username
        for attr in ('creation_user', 'update_user', 'effective_user'):
            usr = getattr(obj, attr)
            self.assertEqual(
                usr.username, user_name,
                msg.format(
                    instance_class_name(obj),
                    attr, usr.username, index))

    def verify_enabled(self, index, obj, expected=True):
        """Verify instance enabled."""
        self.assertEqual(
            obj.enabled, expected,
            self._attribute_msg(obj, 'enabled', index, expected))

    def verify_deleted(self, index, obj, expected=False):
        """Verify instance deleted."""
        self.assertEqual(
            obj.deleted, expected,
            self._attribute_msg(obj, 'deleted', index, expected))

    def verify_version(self, index, obj, expected=1):
        """Verify instance version."""
        self.assertEqual(
            obj.version, expected,
            self._attribute_msg(obj, 'version', index, expected))

    def verify_derived(self, index, obj):
        """
        Verify derived instances.
        Designed for sub class implementation.
        """
        pass

#
#     def check_creation(self, model_class_name, count=1, version=1, **kwargs):
#         klass = self.factory_for(model_class_name)
#         objects = klass.create_instances(count=count, **kwargs)
#         self.verify_instance(model_class_name, objects,
#                              count=count, version=version, **kwargs)
#
#         return objects
#
#     def check_deletion(self, model_class_name, objects):
#         for obj in objects:
#             mngr = self.manager_for(model_class_name)
#             saved_id = obj.id
#             mngr.get(pk=saved_id)
#             obj.delete()
#             with self.assertRaises(mngr.model.DoesNotExist):
#                 mngr.get(pk=saved_id)
#
#     def check_name_update(self, model_class_name, objects):
#         for obj in objects:
#             saved_name = obj.name
#             saved_version = obj.version
#             obj.name = model_class_name
#             obj.save()
#             mngr = self.manager_for(model_class_name)
#             update_1_obj = mngr.get(full_name=model_class_name)
#             update_1_obj.name = saved_name
#             update_1_obj.save(update_fields=['version',
#                                              'full_name', 'short_name'])
#             update_2_obj = mngr.get(full_name=saved_name)
#             self.assertTrue(update_2_obj.version == saved_version + 2)
#
#     def check_update(self, model_class_name, objects):
#         for obj in objects:
#             saved_version = obj.version
#             obj.save()
#             mngr = self.manager_for(model_class_name)
#             update_1_obj = mngr.get(id=obj.id)
#             self.assertTrue(update_1_obj.version == saved_version + 1)


class NamedModelTestCase(VersionedModelTestCase):
    def verify_instances(self, instances,
                         count=1, version=1, **kwargs):
        super(NamedModelTestCase, self).verify_instances(
            instances, count, version, **kwargs)

        for index, instance in enumerate(instances):
            self.verify_named_instance(index, instance)

    def verify_named_instance(self, index, obj):
        """Verify a named instance"""
        for method in (self.verify_name,):
            method(index, obj)

        for attr in ('alias', 'description'):
            attr_value = getattr(obj, attr)
            self.assertTrue(
                attr_value is None,
                '{} {} is not  None at {}'.format(instance_class_name(obj),
                                                  attr,
                                                  index))

    def verify_name(self, index, obj):
        """Verify name field.
        """
        self.assertTrue(
            obj.name,
            '{} name is None at {}'.format(instance_class_name(obj), index))


def create_instances(klass, count, *args, **kwargs):
    """Create instances for class."""
    objects = [klass(*args, **kwargs)
               for _ in range(count)]
    return objects


def randam_ip(n):  # @UnusedVariable
    """Return ramdon ip.
    """

    not_valid = [10, 127, 169, 172, 192]

    first = randrange(1, 256)
    while first in not_valid:
        first = randrange(1, 256)

    ip = ".".join([str(first), str(randrange(1, 256)),
                   str(randrange(1, 256)), str(randrange(1, 256))])
    return ip


def create_named_instances(klass, names, *args, **kwargs):
    """Create named instances utility function."""
    objects = [klass(short_name=name, full_name=name, *args, **kwargs)
               for name in names]
    return objects


def generate_name(seed, index):
    """Name generator function.
    """
    base_name = inflection.underscore(seed).upper()
    return '{}_{}'.format(base_name, index)


def generate_names(seed, count):
    """Names generator function"""
    names = [generate_name(seed, index) for index in range(1, count + 1)]
    return names


def test_data_file_path(file_name, dir_name=None):
    """Return test data file path.
    """
    try:
        dir_name = dir_name or settings.TEST_DATA_DIR
    except AttributeError:
        dir_name = os.path.join(settings.PROJECT_ROOT, 'tests/data')
    return os.path.join(dir_name, file_name)


def factory_class_name(model_class_name):
    """Return factory class name from model class"""
    return model_class_name + 'Factory'
