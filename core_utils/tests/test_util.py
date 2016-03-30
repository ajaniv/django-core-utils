"""

..  module:: omcore.utils.tests.test_util.py
    :synopsis: Unit test utilities module

"""

import os
import inflection
from random import randrange

from django.conf import settings
from django.test import TestCase

from ..utils import current_site
from . import factories

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
        TestCaseMixin.setUp(self)
        TestCase.setUp(self)

    def tearDown(self):
        TestCaseMixin.tearDown(self)
        TestCase.tearDown(self)


class VersionedModelTestCase(BaseAppDjangoTestCase):
    pass
#     def verify_instance(self, class_name, objects,
#                         count=1, version=1, **kwargs):
#         self.assertEqual(len(objects), count,
#             '%s error:  instance count error; expected:%d allocated:%d' % (
#                 class_name, count, len(objects)))
#
#         for index, obj in enumerate(objects):
#             self.verify_instance_enabled(class_name, index, obj)
#             self.assertFalse(obj.deleted,
#                 '%s error: instance is deleted ' % class_name)
#             self.assertEqual(obj.version, version,
#                 '%s error: instance version %d' % (
#                         class_name, obj.version))
#
#             self.verify_instance_name(class_name, index,  obj)
#
#             self.assertEqual(
#                 obj.creation_user.username, obj.update_user.username,
#                 '%s error: user  mismatch full: %s short: %s' % (
#                     class_name, obj.creation_user.username,
#                     obj.update_user.username))
#
#             self.assertTrue(
#                 obj.creation_time <= obj.update_time,
#                 '%s error: time mismatch creation: %s update: %s' % (
#                     class_name, obj.creation_time.microsecond,
#                     obj.update_time.microsecond))
#
#             self.verify_derived(class_name, index, obj)
#
#     def verify_derived(self, class_name, index, obj):
#         pass
#
#     def verify_instance_name(self, *args, **kwargs):
#         pass
#
#     def verify_instance_enabled(self, class_name, index, obj):
#         self.assertTrue(obj.enabled,
#             '%s error: instance not enabled' % class_name)
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


class NamedInstanceTestCase(VersionedModelTestCase):
    pass

#     def verify_instance_name(self, class_name, index, obj):
#         self.assertTrue(obj.full_name  is not None,
#                 '%s error: instance full name is None')
#         self.assertTrue(obj.short_name is not None,
#                 '%s error: short name is None')
#         self.assertEqual(obj.full_name, obj.short_name,
#             '%s error: instance name mismatch full: %s short: %s' % (
#                     class_name, obj.full_name, obj.short_name))
#         self.assertEqual(obj.short_name,
#                generate_name(class_name, index + 1),
#             '%s error: invalid names full: %s short: %s' % (
#                     class_name, obj.full_name, obj.short_name))


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
