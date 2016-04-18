"""

..  module:: django_core_utils.admin
    :synopsis: django_core_utils admin core functionality.

django_core_utils admin core functionality.


"""
from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.sites.shortcuts import get_current_site
from python_core_utils.core import class_name

from .forms import GroupAdminForm, NamedModelAdminForm, VersionedModelAdminForm

DISPLAY_NAME_SIZE = 32


def create_admin_class(target_class_name,
                       base_classes,
                       attrs):
    """
    Dynamically create instance of admin class
    """
    return type(
        target_class_name,
        base_classes,
        attrs)


def admin_class_name(clasz):
    """
    Format admin class name
    """
    return class_name(clasz) + "Admin"


def admin_site_register(clasz, base_classes, attrs):
    """
    Register model class with admin site
    Dynamically create the associated admin class
    """

    admin.site.register(
        clasz,
        create_admin_class(
            admin_class_name(clasz),
            base_classes,
            attrs))


def name_model_fields():
    """return named model fields"""
    return (("name",), ("alias",), ("description",))


def named_model_field_sets(model_name):
    """return named model common field set.
    """
    return ((model_name,
             {'fields': name_model_fields()}),
            ) + NamedModelAdmin.get_field_sets()


def named_model_admin_class_attrs(model_name):
    """
    Generate named admin class meta attrs
    """
    return dict(fieldsets=named_model_field_sets(model_name))


def system_fields():
    """return system fields"""
    return (("id",),
            ("uuid",),
            ("version"),
            ("site",))


def system_field_set():
    """return system fields set"""
    return ("System", {
            "classes": ("collapse",),
            "fields": system_fields(),
            })


def audit_fields():
    """return audit fields"""
    return(("effective_user",),
           ("update_time",), ("update_user",),
           ("creation_time",), ("creation_user",))


def audit_field_set():
    """return audit fields set"""
    return ("Audit", {
            "classes": ("collapse",),
            "fields": audit_fields(),
            })


def detail_fields():
    """return detail fields"""
    return("enabled", "deleted")


def detail_field_set():
    """return detail fields set"""
    return ("Details",
            {
                "classes": ("collapse",),
                "fields": detail_fields()
            })


def core_display_list_fields():
    """
    Return list of fields displayed in all change lists
    """
    return ("id", "update_time", "update_user")


class GroupAdmin(GroupAdmin):
    """
    Override GroupAdmin to allow user management
    """
    form = GroupAdminForm


class VersionedModelAdmin(admin.ModelAdmin):
    """Versioned model admin class.
    """
    form = VersionedModelAdminForm
    list_display = ("id", "version", "update_time", "update_user")
    list_filter = ("update_time",)
    date_hierarchy = "update_time"
    exclude = tuple()
    readonly_fields = (
        "id", "creation_time", "creation_user", "deleted",
        "site", "update_time", "update_user", "effective_user",
        "uuid", "version")
    ordering = ("id",)

    def save_model(self, request, obj, form, change):
        """Given a model instance save it to the database.

        Override save model implementation.
        """
        self.prepare(request, obj, form, change)
        super(VersionedModelAdmin, self).save_model(request, obj, form, change)

    def prepare(self, request, obj, form, change):
        """Subclass hook to prepare for saving.
        """
        self.prepare_system_fields(request, obj,
                                   form, change)

    def prepare_system_fields(self, request, obj, form, change):
        """Populate system related fields.
        """
        if obj.id is None:
            obj.creation_user = request.user
            obj.site = get_current_site(request)
        obj.update_user = request.user
        obj.effective_user = request.user

    @classmethod
    def get_field_sets(clasz):
        """return field set."""
        return (detail_field_set(),
                audit_field_set(),
                system_field_set())


class NamedModelAdmin(VersionedModelAdmin):
    """
    Named model admin class.
    """
    form = NamedModelAdminForm
    list_display = ("id", "get_name", "update_time", "update_user")
    list_display_links = ("id", "get_name", )
    list_filter = ("name",) + VersionedModelAdmin.list_filter
    search_fields = ("name",)
    ordering = ("name",)

    def get_name(self, instance):
        """return instance name."""
        return instance.name[:DISPLAY_NAME_SIZE]
    get_name.short_description = "name"
