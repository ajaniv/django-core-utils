"""
.. module::  django_core_utils.serializers
   :synopsis:  django_core_utils Django rest framework serializers module.

django_core_utils Django rest framework serializers module.
"""
from __future__ import absolute_import
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import validators
from rest_framework import serializers

from . import models
from . import constants
from .utils import current_site
from .fields import im_schemes

CREATION_USER = "creation_user"
EFFECTIVE_USER = "effective_user"
SITE = "site"
UPDATE_USER = "update_user"
USER = "user"


class UserSerializer(serializers.ModelSerializer):
    """User model serializer class."""
    class Meta:
        model = User
        fields = ('id', 'username')


class VersionedModelSerializer(serializers.ModelSerializer):
    """Base class for versioned model serializers."""

    creation_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False)
    effective_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False)
    update_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False)
    site = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.all(), required=False)

    class Meta:
        """Meta class definition."""
        model = models.VersionedModel
        fields = ('id', 'uuid', 'version', 'enabled', 'deleted',
                  'creation_time', 'update_time',
                  CREATION_USER, UPDATE_USER, EFFECTIVE_USER,
                  SITE)

    def _add_missing(self, attrs):
        """Add missing attributes."""
        request = self.context.get("request")
        if request:
            user = getattr(request, USER, None)
            site = current_site(request)
            attr_names = (EFFECTIVE_USER, UPDATE_USER)
            attr_values = (user, user)

            if request.method == constants.HTTP_POST:
                attr_names = attr_names + (SITE, CREATION_USER)
                attr_values = attr_values + (site, user)

            for attr, value in zip(attr_names, attr_values):
                if attr not in attrs:
                    attrs[attr] = value
        return attrs

    def validate(self, attrs):
        """Perform cross field validation.
        """
        attrs = self._add_missing(attrs)
        import copy
        # @TODO: with Django 2.1.1 and Python 3.7
        # require merging of attributes with instance to
        # pass validation - root cause
        # is not clear; could be application error
        if self.partial:
            instance = copy.deepcopy(self.instance)
            for key in attrs.keys():
                setattr(instance, key, attrs[key])
        else:
            # @TODO: does not feel correct to create an
            # instance in order to reuse the model validation.
            instance = self.Meta.model(**attrs)
        instance.clean()
        return attrs


class BaseNamedModelSerializer(VersionedModelSerializer):
    """Base class for named model serializers."""

    class Meta(VersionedModelSerializer.Meta):
        """Meta class definition."""
        model = models.VersionedModel
        fields = VersionedModelSerializer.Meta.fields + ("name", "alias",
                                                         "description")


class NamedModelSerializer(BaseNamedModelSerializer):
    """Base class for named model(required) serializers."""

    class Meta(BaseNamedModelSerializer.Meta):
        """Meta class definition."""
        model = models.NamedModel


class OptionalNamedModelSerializer(BaseNamedModelSerializer):
    """Base class named model(optional) serializers."""

    class Meta(BaseNamedModelSerializer.Meta):
        """Meta class definition."""
        model = models.OptionalNamedModel


class PrioritizedModelSerializer(VersionedModelSerializer):
    """Base class for prioritized model serializers."""

    class Meta(VersionedModelSerializer.Meta):
        """Meta class definition."""
        model = models.PrioritizedModel
        fields = VersionedModelSerializer.Meta.fields + ("priority",)


class InstantMessagingField(serializers.CharField):
    """InstantMessaing field class."""
    default_error_messages = {
        'invalid': _('Enter a valid URL.')
    }

    def __init__(self, **kwargs):
        super(InstantMessagingField, self).__init__(**kwargs)
        validator = validators.URLValidator(
            schemes=im_schemes, message=self.error_messages['invalid'])
        self.validators.append(validator)
