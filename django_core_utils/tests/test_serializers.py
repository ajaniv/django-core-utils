"""
.. module::  django_core_utils.tests.test_serializers
   :synopsis: django_core_utils serializers unit test module.

*django_core_utils* serializers unit test module.
"""
from __future__ import absolute_import, print_function

from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from ..models import NamedModel
from ..serializers import NamedModelSerializer

_app_label = 'test_serializers'


class SampleSerializedModel(NamedModel):
    """Sample model class."""
    class Meta(NamedModel.Meta):
        """Meta model class."""
        app_label = _app_label


class SampleModelSerializer(NamedModelSerializer):
    """Sample serializer class."""
    class Meta(NamedModelSerializer.Meta):
        """Meta class definition."""
        model = SampleSerializedModel


class BasicSerializerTestCase(TestCase):
    """Serializer unit test class.

    This unit test is designed to verify basic integration
    with Django's rest framework components.  It is constrained
    to serialization - no underlying db tables are in place.
    """
    def test_model_serialization(self):

        instance = SampleSerializedModel(name="my_name")
        serializer = SampleModelSerializer(instance)
        serialized_data = serializer.data

        self.assertTrue(isinstance(serialized_data, dict),
                        "serialized data is not dict")
        content = JSONRenderer().render(serialized_data)
        self.assertTrue(isinstance(content, bytes),
                        'content is not bytes')
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        self.assertTrue(isinstance(data, dict),
                        "de-serialized data is not dict")

        self.assertTrue(SampleModelSerializer(data=data),
                        "serializer creation error")
