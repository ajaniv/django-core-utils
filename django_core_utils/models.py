"""
.. module::  django_core_utils.models
   :synopsis:  django_core_utils core  models module.

Shared django_core_utils core  models module.
"""
from __future__ import absolute_import

import logging

import inflection
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from python_core_utils.core import class_name, instance_class_name

from . import constants, fields

logger = logging.getLogger(__name__)


def verbose_class_name(name):
    """Generate verbose name from class name.
    """
    verbose_name = inflection.underscore(name)
    verbose_name = verbose_name.replace('_', ' ')
    return verbose_name


def pluralize(name):
    """Pluralize a name.
    """
    return inflection.pluralize(name)


def db_table_for_class(name):
    """Convert class name to db table name.
    """
    table_name = inflection.underscore(name)
    return table_name


def db_table_for_app_and_class(app_name, table_name, site_label):
    """Generate application table name.
    """
    site_label = site_label or constants.SITE_LABEL
    return '{}_{}_{}'.format(site_label, app_name, table_name)


def db_table(app_name, name, site_label=None):
    """Generate db table name from app and class.
    """
    return db_table_for_app_and_class(
        app_name, db_table_for_class(name), site_label)


class VersionedModelManager(models.Manager):
    """Versioned object manager class.
    """

    def get_or_none(self, *args, **kwargs):
        """Return an object instance or none.

        :param args: Positional argument list.
        :type args: list.
        :param kwargs: Key words arguments.
        :type kwargs: dict.
        :returns:  An instance of Model or None.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


@python_2_unicode_compatible
class VersionedModel(models.Model):
    """An abstract base class for application object versioning.
    """

    id = fields.auto_field()
    uuid = fields.uuid_field()
    version = fields.integer_field()
    enabled = fields.boolean_field(default=True)
    deleted = fields.boolean_field(default=False)
    creation_time = fields.datetime_field(auto_now_add=True)
    update_time = fields.datetime_field(auto_now=True)

    # user who created the instance
    creation_user = fields.user_field(
        related_name="%(app_label)s_%(class)s_related_creation_user")

    # user who triggered the instance update
    update_user = fields.user_field(
        related_name="%(app_label)s_%(class)s_related_update_user")

    # user on whose behalf change is made
    effective_user = fields.user_field(
        related_name="%(app_label)s_%(class)s_related_effective_user")

    site = fields.foreign_key_field(
        Site,
        related_name="%(app_label)s_%(class)s_related_site")

    objects = VersionedModelManager()

    class Meta(object):
        """Meta class declaration."""
        abstract = True
        get_latest_by = 'update_time'

    def __init__(self, *args, **kwargs):
        super(VersionedModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save an instance.
        """
        self.version += 1
        super(VersionedModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{0} object {1.id!s} {1.uuid!s} {1.version!s}'.format(
            instance_class_name(self), self)


class NamedModelManager(VersionedModelManager):
    """Named object manager class.
    """
    def named_instance(self, name):
        """Find a named instance.
        """
        try:
            return self.get(name=name)
        except self.model.DoesNotExist:
            logger.warning(
                'Failed to retrieve instance of type (%s) named (%s)',
                class_name(self.model), name)
            return self.get(name=constants.UNKNOWN)


class BasedNamedModel(VersionedModel):
    """Abstract base class for named model instances.

    Designed to facilitate the capture of static reference data
    types such as countries, currencies, and languages.
    """
    alias = fields.name_field(blank=True, null=True, unique=False)
    description = fields.description_field(blank=True, null=True)

    class Meta(VersionedModel.Meta):
        """Model meta class declaration."""
        abstract = True
        ordering = ("name",)

    objects = NamedModelManager()

    @property
    def display_name(self):
        """Return display name."""
        return self.alias if self.alias else self.name

    def __str__(self):
        # TODO: in python 2.7 calling super results in recursion
        return '{0.display_name!s}'.format(self)


class NamedModel(BasedNamedModel):
    """Abstract base class for required 'named' model instances.

    """
    name = fields.name_field()

    class Meta(BasedNamedModel.Meta):
        """Model meta class declaration."""
        abstract = True


class OptionalNamedModel(BasedNamedModel):
    """Abstract base class for optional 'named' model instances.

    """
    name = fields.name_field(blank=True, null=True, unique=False)

    class Meta(BasedNamedModel.Meta):
        """Model meta class declaration."""
        abstract = True


class PrioritizedModel(models.Model):
    """An abstract base class for models requiring priority.
    Associate a priority with an instance.
    """
    class Meta(object):
        """Model meta class declaration."""
        abstract = True

    priority = fields.priority_field()
