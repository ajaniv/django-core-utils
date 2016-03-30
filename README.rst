==========
core_utils
==========

*core_utils* is a reusable Django app.  It is primarily intended for applications
which need to maintain an audit trail of database changes. 

It was developed using Django 1.9.4 for python 2.7 and python 3.5.
A separate project *django_utils_test* was created to test the abstract classes
because of Django's limitations in handling model classes created witin
the scope of a unit test.

Detailed documentation is in the "docs" directory.

Quick start
-----------
1. The application requires 'django.contrib.sites' to be added to
   INSTALLED_APPS, and an SITE_ID configured.
2. Add "core_utils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'core_utils',
    ]

Key Classes
-----------
VersionedModel
^^^^^^^^^^^^^^
Abstract base model class with basic audit trail fields:

* creation_user
* update_user
* effective_user
* creation_time
* update_time

NamedModel
^^^^^^^^^^
Abstract class derived from VersionedModel which  adds fields typically required
by reference data classes:

* name
* alias
* description

PrioritizedModel
^^^^^^^^^^^^^^^^
Abstract class derived from VersionedModel which adds fields required for 
instance priority (i.e. which of a contact's address has the highest priority):

* priority

Dependencies
------------

Runtime
^^^^^^^

* python_utils
* django-macaddress
* django-phonenumber-field
* django-timezone-field
* inflection
* phonenumbers

Development
^^^^^^^^^^^

* coverage
* flake8
* tox
* virtualenv

Notes
^^^^^

* pandoc was used to convert from .rst to .md:

  ``pandoc -f rst -t markdown_github -o README.md README.rst``
  
* check-manifest was run from the command line.  Could not get it
  to work from within tox.  There was an error in handling '~'
  with gitconfig when running:
  
  ``git ls-files -z``