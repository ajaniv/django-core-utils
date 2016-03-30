"""
.. module::  core.tests.factories
   :synopsis:  django-utils core factory module.

*django-utils* core factory module.
"""
import uuid as _uuid
import factory

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from utils.core import class_name
from ..models import VersionedModel, NamedModel


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
        django_get_or_create = ('id',)

    id = 1


def model_class_name(factory_class):
    """Return model class name for factory class.
    """
    return class_name(factory_class.Meta.model)


def default_name(cls, number):
    """Return a default name for given class.
    """
    return '{}_{}'.format(class_name(cls), number)


class VersionedModelFactory(factory.DjangoModelFactory):
    """Versioned model factory class."""
    class Meta(object):
        """Model meta class."""
        model = VersionedModel
        abstract = True
        django_get_or_create = ('id', 'uuid')

    creation_user = factory.SubFactory(UserFactory)
    update_user = factory.SubFactory(UserFactory)
    effective_user = factory.SubFactory(UserFactory)
    site = factory.SubFactory(SiteFactory)
    enabled = True
    deleted = False

    id = factory.Sequence(lambda n: n)
    uuid = factory.Sequence(lambda _: _uuid.uuid4())

    @classmethod
    def model_class_name(cls):
        """Return model class name."""
        return model_class_name(cls)

    @staticmethod
    def default_name(number):
        """Return default name.
        """
        return '{}_{}'.format(model_class_name(), number)


class NamedModelFactory(VersionedModelFactory):
    """Named model factory class."""
    class Meta(object):
        """Model meta class."""
        model = NamedModel
        abstract = True
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: VersionedModelFactory.default_name(n))
    alias = factory.Sequence(lambda n: VersionedModelFactory.default_name(n))
