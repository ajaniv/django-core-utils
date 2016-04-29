"""
.. module::  django_core_utils.views
   :synopsis:  django_core_utils views module.

django_core_utils views module.
There are multiple techniques to handle api requests:
- Function end points
- Class based views derived from APIView
- Usage of mixin classes.

Which technique is best for a given problem is often a subjective decision.
That is the reason why the implementation below supports these options.

"""
from __future__ import absolute_import

from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import constants
from .serializers import UserSerializer


def instance_list(request, model_class,
                  serializer_class, content_format=None):
    """
    List all versioned model instances, or create a new instance.
    """
    if request.method == constants.HTTP_GET:
        instances = model_class.objects.all()
        serializer = serializer_class(instances, many=True)
        return Response(serializer.data)

    elif request.method == constants.HTTP_POST:
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


def instance_detail(request, pk, model_class,
                    serializer_class, content_format=None):
    """Fetch, update or delete versioned model instance.
    """
    try:
        snippet = model_class.objects.get(pk=pk)
    except model_class.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == constants.HTTP_GET:
        serializer = serializer_class(snippet)
        return Response(serializer.data)

    elif request.method == constants.HTTP_PUT:
        serializer = serializer_class(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == constants.HTTP_DELETE:
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObjectListView(GenericAPIView):
    """Base class for versioned model listing of all objects,
    or create a new object.
    Derived classes are expected to define two class level attributes:
    - queryset = ModelClass.objects.all()
    - serializer_class = SerializerClass
    """

    def get(self, request, content_format=None):
        objects = self.get_queryset()
        serializer = self.get_serializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, content_format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDetailView(GenericAPIView):
    """Base class for versioned models to get, update or delete an instance.
    Derived classes are expected to define to class level attributes:
    - queryset = ModelClass.objects.all()
    - serializer_class = SerializerClass
    """

    def get(self, request, pk, content_format=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, content_format=None):
        instance = self.get_object()
        # Note the partial update setting
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, content_format=None):
        snippet = self.get_object()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObjectListMixin(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """Base class for versioned models list and post using mixins.
    Derived classes are expected to define to class level attributes:
    - queryset = ModelClass.objects.all()
    - serializer_class = SerializerClass
    """
    # queryset = ModelClass.objects.all()
    # serializer_class = SerializerClass

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ObjectDetailMixin(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """Base class for versioned models list and post using mixins.
    Derived classes are expected to define to class level attributes:
    - queryset = ModelClass.objects.all()
    - serializer_class = SerializerClass
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Note the partial update setting
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    """List all users, or create a new user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """Fetch, update or delete versioned model instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
