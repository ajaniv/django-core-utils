
=================
django_core_utils
=================

*django_core_utils* is a reusable Django component primarily intended for applications
which need to maintain an audit trail of database changes,  develop a consistent
business object model, and expose REST API end points. The consistent business object
model development is facilitated with a set of common model base classes and helper functions
for field creation.

It was developed using Django 1.9.4 for python 2.7 and python 3.5.
A separate project *django_utils_test* was created to test the abstract classes
because of Django's limitations in handling model classes created within
the scope of a unit test.

A set of base classes which simplify the development of REST API components
has been implemented using `djangorestframework`_.

Detailed documentation may be found "docs" directory.


Build Status
------------

.. image:: https://travis-ci.org/ajaniv/django-core-utils.svg?branch=master
    :target: https://travis-ci.org/ajaniv/django-core-utils


Quick start
-----------
1. The application requires 'django.contrib.sites' to be added to
   INSTALLED_APPS, and an SITE_ID configured.
2. Add "core_utils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_core_utils',
    ]

Key Model Classes
-----------------
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

Key Django Rest API Classes
---------------------------

Serializers
^^^^^^^^^^^

* VersionedModelSerializer.
* NamedModelSerializer
* PrioritizedModelSerializer

Views
^^^^^

* ObjectListView
* ObjectDetailView

Dependencies
------------

Runtime/Development
^^^^^^^^^^^^^^^^^^^

* python_core_utils
* django-macaddress
* django-phonenumber-field
* django-timezone-field
* inflection
* phonenumbers
* `djangorestframework`_.

Development
^^^^^^^^^^^

* coverage
* flake8
* tox
* virtualenv

Notes
^^^^^

* pandoc can be used to convert from .rst to .md:

  ``pandoc -f rst -t markdown_github -o README.md README.rst``
  
* check-manifest was run from the command line.  Could not get it
  to work from within tox.  There was an error in handling '~'
  with gitconfig when running:
  
  ``git ls-files -z``
  
To do
-----
* Generate sphinix and/or markup documentation.
* Review approach to hand crafted model class, unit test, serializer generation.
  Portions of these can be generated using scripts, albeit with reduced readability
  and increased risk of incompatibility with future Django and Django Rest Framewrok
  releases.
* Django rest framework mixin classes usage needs to be reviewed.
  
 .. _djangorestframework: http://www.django-rest-framework.org/