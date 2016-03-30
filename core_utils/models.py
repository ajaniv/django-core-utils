"""
.. module::  core.models
   :synopsis:  Shared Django-utils core  models module.

Shared Django-utils core  models module.
"""
from __future__ import absolute_import
import logging
import inflection

from django.contrib.sites.models import Site


from django.db import models

from utils.core import class_name
from . import fields
from . import constants


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


class VersionedModel(models.Model):
    """An abstract base class for application object versioning.
    """
    class Meta(object):
        """Meta class declaration."""
        abstract = True
        get_latest_by = 'update_time'

    objects = VersionedModelManager()
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

    def __init__(self, *args, **kwargs):
        super(VersionedModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save an instance.
        """
        self.version += 1
        update_user = kwargs.pop("update_user", None)
        if update_user is not None:
            self.update_user = update_user
        effective_user = kwargs.pop("effective_user", None)
        if update_user is not None:
            self.effective_user = effective_user
        super(VersionedModel, self).save(*args, **kwargs)


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


class NamedModel(VersionedModel):
    """Abstract base class for named model instances.

    Designed to facilitate the capture of static reference data
    types such as countries, currencies, and languages.
    """
    class Meta(VersionedModel.Meta):
        """Model meta class declaration."""
        abstract = True
        ordering = ("name",)

    objects = NamedModelManager()
    name = fields.name_field()
    alias = fields.name_field(blank=True, null=True, unique=False)
    description = fields.description_field(blank=True, null=True)

    @property
    def display_name(self):
        """Return display name."""
        return self.alias if self.alias else self.name

    def __str__(self):
        return self.display_name


class PrioritizedModel(models.Model):
    """An abstract base class for models requiring priority.
    Associate a priority with an instance.
    """
    class Meta(object):
        """Model meta class declaration."""
        abstract = True

    priority = fields.priority_field()
