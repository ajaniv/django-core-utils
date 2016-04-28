"""
.. module::  django_core_utils.serializers
   :synopsis:  django_core_utils Django rest framework serializers module.

django_core_utils Django rest framework serializers module.
"""
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from rest_framework import serializers

from . import models
from .utils import current_site

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

    def validate(self, attrs):
        """Perform cross field validation.
        """

        request = self.context.get("request")
        if request:
            user = getattr(request, USER, None)
            site = current_site(request)
            model_attrs = (SITE, CREATION_USER, EFFECTIVE_USER, UPDATE_USER)
            attr_values = (site, user, user, user)
            for attr, value in zip(model_attrs, attr_values):
                if attr not in attrs:
                    attrs[attr] = value

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
