from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import User

from crm.filters import ClientFilter, ContractFilter, EventFilter
from crm.models import Client, Contract, Event
from crm.permissions import (
    HasClientPermission,
    HasContractPermission,
    HasEventPermission,
)
from crm.serializers import ClientSerializer, ContractSerializer, EventSerializer
from crm.utils import make_log


class CustomViewset(
    GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    # RetrieveModelMixin,
    UpdateModelMixin,
):
    pass


class ClientViewset(CustomViewset):
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClientFilter
    permission_classes = [IsAuthenticated, HasClientPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.request.method == "GET":
            if self.request.user.department.id == 1:
                return Client.objects.filter(contact=self.request.user.pk)

            if self.request.user.department.id == 2:
                ids_client_user = [
                    event.contract.client.id
                    for event in Event.objects.filter(contact=self.request.user.pk)
                ]
                return Client.objects.filter(id__in=ids_client_user)

        return Client.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("POST", "Client", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(status="POTENTIAL")
        serializer.save(contact=request.user)
        return super(ClientViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Client", key[0], k, request.user)

        return super(ClientViewset, self).update(request, *args, **kwargs)


class ContractViewset(CustomViewset):
    serializer_class = ContractSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContractFilter
    permission_classes = [IsAuthenticated, HasContractPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.request.method in ["GET"]:
            return Contract.objects.filter(contact=self.request.user.pk)
        return Contract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid():
            if Client.objects.filter(
                id=serializer.validated_data["client"].id, contact=request.user.id
            ).exists():
                serializer.save(contact=request.user)
                serializer.save(is_signed=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            message = "You can only create contracts to your related clients"
            make_log("POST", "Contract", "client", message, request.user)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        for key in serializer.errors.items():
            for k in key[1]:
                make_log("POST", "Contract", key[0], k, request.user)

        return super(ContractViewset, self).create(request, *args, **kwargs)

    #     return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Contract", key[0], k, request.user)

        if serializer.is_valid():
            if instance.is_signed:
                message = "You can't update a signed contract"
                make_log("PUT", "Contract", None, message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            if (instance.is_signed is False) and (
                serializer.validated_data["is_signed"] is True
            ):
                Event.objects.create(contract_id=instance.id)
            return super(ContractViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_signed:
            message = "You can't delete a signed contract"
            make_log("DELETE", "Contract", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return super(ContractViewset, self).destroy(request, *args, **kwargs)


class EventViewset(CustomViewset):
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated, HasEventPermission]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.request.method in ["GET"]:
            return Event.objects.filter(contact=self.request.user.pk)
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("POST", "Event", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_qs = User.objects.filter(id=request.data["contact"])
        if user_qs[0].department_id != 2:
            message = "The contact must be a support contact"
            make_log("POST", "Event", "contact", message, request.user)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return super(EventViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Event", key[0], k, request.user)

        if instance.is_finished:
            message = "You can't update a finished event"
            make_log("PUT", "Event", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        return super(EventViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_finished:
            message = "You can't delete a finished event"
            make_log("DELETE", "Event", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return super(EventViewset, self).destroy(request, *args, **kwargs)
