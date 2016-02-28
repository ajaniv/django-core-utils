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

setup(
    name='django-utils',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A collection of reusable Django components',
    long_description=README,
    url='http://www.ondalear.com/',
    author='Amnon Janiv',
    author_email='amnon.janiv@ondalear.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
