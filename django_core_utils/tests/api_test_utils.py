"""
..  module:: django_core_utils.tests.api_test_utils.py
    :synopsis: API Unit test utilities module.
API Unit test utilities module.
"""
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .test_utils import TestCaseMixin


class BaseApiTestCase(TestCaseMixin, APITestCase):
    """Base Django rest framework api test case class"""
    def setUp(self):
        APITestCase.setUp(self)
        TestCaseMixin.setUp(self)

    def tearDown(self):
        TestCaseMixin.tearDown(self)
        APITestCase.tearDown(self)


class VersionedModelApiTestCase(BaseApiTestCase):
    """Base class for versioned model api unit tests.
    """
    def post_required_data(self, user=None, site=None):
        """return versioned model post request required data."""
        user_id = user.id if user else self.super_user.id
        site_id = site.id if site else self.site.id
        return dict(
            creation_user=user_id,
            effective_user=user_id,
            update_user=user_id,
            site=site_id)

    def setUp(self):
        super(VersionedModelApiTestCase, self).setUp()
        self.assertTrue(self.client.login(username=self.TEST_SUPER_USER_NAME,
                        password=self.TEST_PASSWORD),
                        'api client login failed')

    def tearDown(self):
        self.client.logout()
        super(VersionedModelApiTestCase, self).tearDown()

    def verify_create(self, url_name, data, model_class):
        """verify post request for versioned model instance creation."""
        url = reverse(url_name)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(model_class.objects.count(), 1)
        instance = model_class.objects.get()
        return response, instance


class NamdedModelApiTestCase(VersionedModelApiTestCase):
    """Base class for named model api unit tests.
    """
    def post_required_data(self, user=None, site=None):
        """Return named model post request required data."""
        data = super(NamdedModelApiTestCase, self).post_required_data(user,
                                                                      site)
        data.update(dict(name=self.name))
        return data

    def verify_create(self, url, data, model_class, expected_name=None):
        """Verify post request for named model instance creation."""
        response, instance = super(
            NamdedModelApiTestCase, self).verify_create(url, data, model_class)
        if expected_name:
            self.assertEqual(instance.name, expected_name)
        return response, instance

    def verify_create_defaults(self, data=None):
        """Verify post request will all required arguments.

        Pulls the required parameters from the test class.
        """
        data = data or self.post_required_data()
        return self.verify_create(
            url=self.url_list,
            data=data,
            model_class=self.model_class,
            expected_name=self.name)

    def verify_create_defaults_partial(self):
        """Verify post request with partial required arguments.

        Pulls the required parameters from the test class.
        """
        return self.verify_create_defaults(data=dict(name=self.name))
