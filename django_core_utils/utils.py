"""
.. module::  django_core_utils.utils
   :synopsis:  django_core_utils simple Django utilities module.

The *utils* module is a collection of Django utility functions.

"""
from django.contrib.sites.models import Site
from django.utils import timezone


def current_site(request=None):
    """Return site instances.
    """
    return Site.objects.get_current(request)


def oldest_timestamp():
    """Return oldest environment timestamp
    """
    return timezone.now().replace(year=2000, month=1, day=1,
                                  hour=0, minute=0, second=0,
                                  microsecond=0)
