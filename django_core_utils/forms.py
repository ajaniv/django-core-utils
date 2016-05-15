"""

..  module:: django_core_utils.forms
    :synopsis: django_core_utils form  utilities.


django_core_utils form  utilities.

"""
from __future__ import absolute_import

from django.core import validators
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group, User

from python_core_utils.core import dict_merge

from . import models
from . import text
from . import fields


class VersionedModelAdminForm(forms.ModelForm):
    """Versioned model admin form class.
    """
    class Meta:
        """Meta class declaration."""
        model = models.VersionedModel
        labels = text.versioned_model_labels
        help_texts = text.versioned_model_help_texts
        fields = '__all__'

    @classmethod
    def labels(clasz):
        return clasz.Meta.labels

    @classmethod
    def help_texts(clasz):
        return clasz.help_texts

    def _update_group(self, group, set_name, field_name, commit):
        """
        Utility method for updating many-to-many model field
        Allows grouping of elements to manage which elements
        are in the group
        """
        if commit:
            setattr(group, set_name,
                    self.cleaned_data[field_name])
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                setattr(group, set_name, self.cleaned_data[field_name])
            self.save_m2m = new_save_m2m
        return group


class BasedNamedModelAdminForm(VersionedModelAdminForm):
    """Base named model admin form class.
    """
    class Meta(VersionedModelAdminForm.Meta):
        """Meta class declaration."""
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'cols': 40})
        }
        labels = dict_merge(
            VersionedModelAdminForm.Meta.labels,
            text.named_model_labels)

        help_texts = dict_merge(
            VersionedModelAdminForm.Meta.help_texts,
            text.named_model_help_texts)


class NamedModelAdminForm(BasedNamedModelAdminForm):
    """Named model admin form class.
    """
    class Meta(BasedNamedModelAdminForm.Meta):
        """Meta class declaration."""
        model = models.NamedModel


class OptionalNamedModelAdminForm(BasedNamedModelAdminForm):
    """Optional named model admin form class.
    """
    class Meta(BasedNamedModelAdminForm.Meta):
        """Meta class declaration."""
        model = models.OptionalNamedModel


class GroupAdminForm(forms.ModelForm):
    """
    Admin form with editable user list
    """
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple('Users', False),
        required=False)

    class Meta:
        """Meta class declaration."""
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(GroupAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=commit)

        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']
            self.save_m2m = new_save_m2m
        return group


class PrioritizedModelAdminForm(VersionedModelAdminForm):
    """Prioritized model admin form class.
    """
    class Meta(VersionedModelAdminForm.Meta):
        """Meta class declaration."""
        models = models.PrioritizedModel
        labels = dict_merge(
            VersionedModelAdminForm.Meta.labels,
            text.prioritized_model_labels)

        help_texts = dict_merge(
            VersionedModelAdminForm.Meta.help_texts,
            text.prioritized_model_help_texts)
        fields = '__all__'


class InstantMessagingField(forms.URLField):
    """Instant messaging forms field class."""
    default_validators = [validators.URLValidator(schemes=fields.im_schemes)]
