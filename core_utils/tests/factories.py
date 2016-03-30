"""
.. module::  core.tests.factories
   :synopsis:  django-utils core factory module.

*django-utils* core factory module.
"""
import uuid
import factory

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from utils.core import class_name
from ..models import VersionedModel, NamedModel


class UserFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = User
        django_get_or_create = ('username',)

    username = 'test_user'

    @staticmethod
    def create_users(count=1, prefix='test_user'):
        users = [UserFactory(username='%s_%d' % (prefix, index))
                 for index in range(1, count + 1)]
        return users


class SiteFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Site
        django_get_or_create = ('id',)

    id = 1


class VersionedModelFactory(factory.DjangoModelFactory):
    class Meta(object):
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
    uuid = factory.Sequence(lambda _: uuid.uuid4())

    @staticmethod
    def create_names():
        pass

    @staticmethod
    def create_instances():
        pass


def model_class_name(factory_class):
    return class_name(factory_class.FACTORY_FOR)


def default_name(cls, n):
    return '{}_{}'.format(class_name(cls), n)


class NamedModelFactory(VersionedModelFactory):
    class Meta(object):
        model = NamedModel
        abstract = True
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: NamedModelFactory.default_name(n))
    alias = factory.Sequence(lambda n: NamedModelFactory.default_name(n))

    @staticmethod
    def default_name(n):
        return '{}_{}'.format(class_name(NamedModelFactory.Meta.model), n)
