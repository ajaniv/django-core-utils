"""
.. module::  setup
   :synopsis: A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

_git_url_root = 'git+ssh://git@github.com/ajaniv/'

setup(
    name='django-core-utils',
    version='0.5.0',
    include_package_data=True,
    license='BSD License',  # example license
    description='A collection of reusable low-level Django components',
    long_description=README,
    url='http://www.ondalear.com/',
    author='Amnon Janiv',
    author_email='amnon.janiv@ondalear.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'inflection>=0.3.1',
        'Django>=1.11.0',
        'djangorestframework>=3.3.3',
        'django-macaddress>=1.3.2',
        'django-money>=0.11.4',
        'django-phonenumber-field>=1.0.0',
        'django-timezone-field>=1.3',
        'jsonfield>=2.0.2',
        'phonenumbers>=7.2.6',
        'python-core-utils',
        'py-moneyed>=0.7.0'
    ],
    dependency_links=[
        _git_url_root + 'python-core-utils@v0.5.0#egg=python-core-utils'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    test_suite='runtests.runtests',
)
