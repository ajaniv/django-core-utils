django\_core\_utils
===================

*django\_core\_utils* is a reusable Django app. It is primarily intended for applications which need to maintain an audit trail of database changes.

It was developed using Django 1.9.4 for python 2.7 and python 3.5. A separate project *django\_utils\_test* was created to test the abstract classes because of Django's limitations in handling model classes created witin the scope of a unit test.

Detailed documentation is in the "docs" directory.

Build Status
------------

[![image](https://travis-ci.org/ajaniv/django-core-utils.svg?branch=master)](https://travis-ci.org/ajaniv/django-core-utils)

Quick start
-----------

1.  The application requires 'django.contrib.sites' to be added to INSTALLED\_APPS, and an SITE\_ID configured.
2.  Add "core\_utils" to your INSTALLED\_APPS setting like this:

        INSTALLED_APPS = [
            ...
            'django_core_utils',
        ]

Key Classes
-----------

### VersionedModel

Abstract base model class with basic audit trail fields:

-   creation\_user
-   update\_user
-   effective\_user
-   creation\_time
-   update\_time

### NamedModel

Abstract class derived from VersionedModel which adds fields typically required by reference data classes:

-   name
-   alias
-   description

### PrioritizedModel

Abstract class derived from VersionedModel which adds fields required for instance priority (i.e. which of a contact's address has the highest priority):

-   priority

Dependencies
------------

### Runtime

-   python\_utils
-   django-macaddress
-   django-phonenumber-field
-   django-timezone-field
-   inflection
-   phonenumbers

### Development

-   coverage
-   flake8
-   tox
-   virtualenv

### Notes

-   pandoc was used to convert from .rst to .md:

    `pandoc -f rst -t markdown_github -o README.md README.rst`

-   check-manifest was run from the command line. Could not get it to work from within tox. There was an error in handling '~' with gitconfig when running:

    `git ls-files -z`


