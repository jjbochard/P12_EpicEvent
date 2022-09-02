from crm.models import Client, Contract, Event
from crm.permissions import (
    HasClientPermission,
    HasContractPermission,
    HasEventPermission,
)
from crm.serializers import ClientSerializer, ContractSerializer, EventSerializer
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CustomViewset(
    GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    pass


class ClientViewset(CustomViewset):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, HasClientPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.request.method == "GET":
            return Client.objects.filter(contact=self.request.user.pk)
        return Client.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(status="POTENTIAL")
        serializer.save(contact=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContractViewset(CustomViewset):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, HasContractPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.request.method == "GET":
            return Contract.objects.filter(contact=self.request.user.pk)
        return Contract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(contact=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventViewset(CustomViewset):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, HasEventPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        # if (
        #     self.request.method != "GET"
        #     and self.request.user.department == Department.objects.get(department="SAL")
        # ):
        #     return Client.objects.filter(contact=self.request.user.pk)
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer.save(status="POTENTIAL")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
