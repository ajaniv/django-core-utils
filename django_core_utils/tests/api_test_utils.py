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

    def instance_to_dict(self, instance, serializer_class):
        """Convert an instance to a dict using serializer."""
        serializer = serializer_class(instance)
        return serializer.data

    def verify_create(self, url_name, data, model_class, data_format=None):
        """Verify post rest api request for model instance creation."""
        url = reverse(url_name)
        data_format = data_format or 'json'
        original_count = model_class.objects.count()
        response = self.client.post(url, data, format=data_format)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.data)
        self.assertEqual(model_class.objects.count(),
                         original_count + 1,
                         "unexpected object count for %s" % model_class)
        instance = model_class.objects.filter().order_by('-id')[0]
        return response, instance

    def assert_equal_dict(self, dict1, dict2, excluded):
        if excluded:
            dict1 = dict1.copy()
            dict2 = dict2.copy()
            for name in excluded:
                del dict1[name]
                del dict2[name]

        self.assertEqual(dict1,
                         dict2,
                         "%s does not match %s" % (dict1, dict2))

    def verify_get(self, url_name, instance, serializer_class, excluded=None):
        """Verify rest api get request."""
        url = reverse(url_name, args=[instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ref_data = self.instance_to_dict(instance, serializer_class)
        self.assert_equal_dict(ref_data, response.data, excluded)

        return response

    def create_instance_default(self, **kwargs):
        """Create an instance configured for api test execution.

        Required when super user id  is used for log in.
        """
        user = self.super_user
        return self.factory_class(creation_user=user, update_user=user,
                                  effective_user=user, site=self.site,
                                  **kwargs)

    def verify_get_defaults(self, excluded=None):
        """Verify rest api get request using default class data."""
        return self.verify_get(self.url_detail,
                               self.create_instance_default(),
                               self.serializer_class,
                               excluded)

    def verify_put(self, url_name, instance, data,
                   serializer_class, excluded=None):
        """Verify put rest api request."""
        excluded = excluded or []

        url = reverse(url_name, args=[instance.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = self.instance_to_dict(instance, serializer_class)
        expected_data.update(data)

        to_exclude = excluded + ["update_time", "version"]
        self.assert_equal_dict(expected_data,
                               response.data,
                               to_exclude)

        return response

    def verify_delete(self, url_name, instance):
        """Verify delete rest api request."""
        url = reverse(url_name, args=[instance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        return response

    def verify_delete_default(self):
        """Verify delete using default parameters."""
        instance = self.create_instance_default()
        return self.verify_delete(self.url_detail, instance)


class NamdedModelApiTestCase(VersionedModelApiTestCase):
    """Base class for named model api unit tests.
    """
    def post_required_data(self, user=None, site=None):
        """Return named model post request required data."""
        data = super(NamdedModelApiTestCase, self).post_required_data(user,
                                                                      site)
        data.update(dict(name=self.name))
        return data

    def verify_create(self, url, data, model_class,
                      expected_name=None, data_format=None):
        """Verify post request for named model instance creation."""
        response, instance = super(
            NamdedModelApiTestCase, self).verify_create(
                url, data, model_class, data_format=data_format)
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

    def verify_put_partial(self, excluded=None):
        """Verify partially populated put request."""
        instance = self.create_instance_default()
        data = dict(id=instance.id, name=self.name)
        return self.verify_put(
            self.url_detail, instance, data, self.serializer_class, excluded)
