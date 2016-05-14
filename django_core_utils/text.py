"""

..  module:: django_core_utils.text
    :synopsis: Common text utilities supporting internationalization.

Common text utilities supporting internationalization.
The approach taken eliminates hard coding of text within model classes.
"""

from django.utils.translation import ugettext_lazy as _

# flake8: noqa
# required because of pep8 regression in ignoring disable of E123


versioned_model_labels = {
    "creation_time": _("Creation time"),
    "creation_user": _("Created by"),
    "deleted": _("Deleted"),
    "effective_user": _("Effective user"),
    "enabled": _("Enabled"),
    "id": _("Id"),
    "site": _("Site"),
    "update_time":  _("Update time"),
    "update_user": _("Updated by"),
    "uuid": _("Uuid"),
    "version": _("Version"),

    }

versioned_model_help_texts = {
    "creation_time": _("Instance creation time."),
    "creation_user": _("User who created object instance."),
    "deleted": _("Controls instance logical deletion state."),
    "effective_user": _("User on whose behalf action was performed."),
    "enabled": _("Controls instance enabled state."),
    "id": _("Per entity type unique identifier."),
    "site": _("Site associated with object instance."),
    "update_time": _("Instance last update time."),
    "update_user": _("User who last updated instance."),
    "uuid": _("Universal unique identifier."),
    "version": _("Instance version id."),
    }

named_model_labels = {
    "alias": _("Alias"),
    "description": _("Description"),
    "name": _("Name"),
    }

named_model_help_texts = {
    "alias": _("Alternative name."),
    "description": _("Instance description."),
    "name": _("Instance name."),
    }

prioritized_model_labels = {
    "priority": _("Priority"),
    }

prioritized_model_help_texts = {
    "priority": _("Instance priority."),
    }
