"""
.. module::  core.utils
   :synopsis:  django-utils core simple Django utilities module.

The *utils* module is a collection of Django utility functions.

"""
from django.utils import timezone
from django.contrib.sites.models import Site


def current_site():
    """Return site instances.
    """
    return Site.objects.get_current()


def oldest_timestamp():
    """Return oldest environment timestamp
    """
    return timezone.now().replace(year=2000, month=1, day=1,
                                  hour=0, minute=0, second=0,
                                  microsecond=0)
