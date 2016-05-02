"""

..  module:: django_core_utils.tests.test_utils.py
    :synopsis: Unit test utilities module

Unit test utilities module
"""
from __future__ import absolute_import, print_function

import os
import string
from random import choice, randrange

import inflection
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from python_core_utils.core import class_name, instance_class_name

from . import factories
from ..utils import current_site


class TestCaseMixin(object):
    """
    Unit test mixin class.
    """
    TEST_DOMAIN = "ondalear.com"
    TEST_USER_NAME = "test_user"
    TEST_SUPER_USER_NAME = "test_super_user"
    TEST_PASSWORD = "pass"
    TEST_USER_EMAIL = "{}@{}".format(TEST_USER_NAME, TEST_DOMAIN)

    def file_path(self, file_name):
        return test_data_file_path(file_name)

    def create_super_user(self, username=None, email=None, password=None):
        return User.objects.create_superuser(
            username=username or self.TEST_SUPER_USER_NAME,
            email=email or "{}@{}".format(self.TEST_USER_NAME,
                                          self.TEST_DOMAIN),
            password=password or self.TEST_PASSWORD)

    def create_user(self, username=None, email=None, password=None):
        user = factories.UserFactory(
            username=username or self.TEST_USER_NAME,
            email=email or self.TEST_USER_EMAIL)
        user.set_password(password or self.TEST_PASSWORD)
        user.save()
        return user

    def setUp(self):
        self.super_user = self.create_super_user()
        self.user = self.create_user()

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

    def assert_instance_equal(self, reference, other, attrs=None):
        """Compare two object instances for the given attributes"""
        if attrs:
            for attr in attrs:
                self.assertEqual(getattr(reference, attr),
                                 getattr(other, attr),
                                 "attr %s equality check error" % attr)
        else:
            self.assertEqual(reference, other, "compare error")


class BaseModelTestCase(TestCaseMixin, TestCase):
    """Base Django model test case class"""
    def setUp(self):
        TestCase.setUp(self)
        TestCaseMixin.setUp(self)

    def tearDown(self):
        TestCaseMixin.tearDown(self)
        TestCase.tearDown(self)


class VersionedModelTestCase(BaseModelTestCase):
    """Versioned model unit test class.
    """
    def verify_instance(self, instance, version=1, **kwargs):
        self.verify_instances([instance], count=1, version=version, **kwargs)

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
        test_username = self.user.username
        for attr in ('creation_user', 'update_user', 'effective_user'):
            user = getattr(obj, attr)
            self.assertEqual(
                user.username, test_username,
                msg.format(
                    instance_class_name(obj),
                    attr, user.username, index))

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

    def verify_versioned_model_crud(self, factory_class):
        """Verify versioned model simple crud operations.
        """
        model_class = factory_class.model_class()
        model_class_name = class_name(model_class)

        instance = factory_class()
        self.verify_instance(instance)
        instance.full_clean()
        self.assertEqual(
            1,
            model_class.objects.count(),
            "Missing %s instances after create" % model_class_name)
        fetched = model_class.objects.get(pk=instance.id)
        fetched.save()
        self.assertEqual(
            fetched.version, 2,
            "%s version mismatch after save" % model_class_name)
        fetched.delete()
        self.assertEqual(
            model_class.objects.count(),
            0,
            "%s instance mismatch after delete" % model_class_name)
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
    """Base class for named model unit tests."""
    NAME_1 = "name_1"
    NAME_2 = "name_2"
    NAMES = (NAME_1, NAME_2)

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

    def verify_named_model_crud(self, names, factory_class, get_by_name):
        """Create named model instances and verify simple crud operations.
        """
        instances = []
        for name in names:
            instances.append(factory_class(name=name))
        self.verify_named_instances_crud(
            instances, factory_class, get_by_name)

    def verify_named_instances_crud(self, instances,
                                    factory_class, get_by_name):
        """Verify crud operations on created named instances.
        """
        model_class = factory_class.model_class()
        model_class_name = class_name(model_class)
        for instance in instances:
            self.verify_instance(instance)
            instance.full_clean()
        instance_count = model_class.objects.count()
        self.assertEqual(
            len(instances),
            instance_count,
            "Missing %s instances after create" % model_class_name)
        instance = model_class.objects.get(name=get_by_name)
        instance.name = 'new name'
        instance.save()
        self.assertEqual(
            instance.version, 2,
            "%s version mismatch after save" % model_class_name)
        instance.delete()
        self.assertEqual(
            model_class.objects.count() + 1,
            instance_count,
            "%s instance mismatch after delete" % model_class_name)
        model_class.objects.all().delete()


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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate an id of a given size"""
    return ''.join(choice(chars) for _ in range(size))


def alpha2_iso_generator():
    """2 char ISO code generator
    """
    return id_generator(size=2, chars=string.ascii_uppercase)


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
