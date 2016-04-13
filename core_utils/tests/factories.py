"""
.. module::  core.tests.factories
   :synopsis:  django-utils core factory module.

*django-utils* core factory module.
"""
from __future__ import absolute_import

import uuid as _uuid
from random import randint

import factory
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from utils.core import class_name

from ..models import NamedModel, VersionedModel


def model_class(factory_class):
    """Return model class name .
    """
    return factory_class._meta.model


def model_class_name(factory_class):
    """Return model class name for factory class.
    """
    return class_name(model_class(factory_class))


def default_name(cls, number):
    """Return a default name for given class.
    """
    return '{}_{}'.format(class_name(cls), number)


class UserFactory(factory.DjangoModelFactory):
    """User factory class."""

    class Meta(object):
        """Model meta class."""
        model = User
        django_get_or_create = ('username',)

    username = 'test_user'

    @staticmethod
    def create_users(count=1, prefix='test_user'):
        """Create users method"""
        users = [UserFactory(username='%s_%d' % (prefix, index))
                 for index in range(1, count + 1)]
        return users


class SiteFactory(factory.DjangoModelFactory):
    """Site factory class."""

    class Meta(object):
        """Model meta class."""
        model = Site
        django_get_or_create = ('domain',)

    domain = 'test_domain'


class VersionedModelFactory(factory.DjangoModelFactory):
    """Versioned model factory class."""

    class Meta(object):
        """Model meta class."""
        abstract = True
        model = VersionedModel
        django_get_or_create = ('uuid',)

    creation_user = factory.SubFactory(UserFactory)
    update_user = factory.SubFactory(UserFactory)
    effective_user = factory.SubFactory(UserFactory)
    site = factory.SubFactory(SiteFactory)
    enabled = True
    deleted = False

    uuid = factory.Sequence(lambda _: _uuid.uuid4())

    @classmethod
    def model_class(cls):
        """Return model class."""
        return model_class(cls)

    @classmethod
    def model_class_name(cls):
        """Return model class name."""
        return model_class_name(cls)

    @classmethod
    def default_name(cls, number):
        """Return default name.
        """
        return '{}_{}'.format(model_class_name(cls), number)


class NamedModelFactory(VersionedModelFactory):
    """Named model factory class."""

    class Meta(object):
        """Model meta class."""
        abstract = True
        model = NamedModel
        django_get_or_create = ('name',)

    @factory.lazy_attribute
    def name(self):
        return "NamedModel_{}".format(randint(0, 1000))
