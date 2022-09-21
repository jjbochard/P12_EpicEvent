from django.db import transaction
from django.utils import timezone
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status="POTENTIAL")
            serializer.save(contact=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("POST", "Client", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Client", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return super(ClientViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == "ACTUAL":
            message = "You can only delete potential client"
            make_log("DELETE", "Client", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("POST", "Contract", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            client_to_create_contract = Client.objects.get(
                id=serializer.validated_data["client"].id
            )
            if client_to_create_contract.contact.id != request.user.id:
                message = "You can only create contracts to your related clients"
                make_log("POST", "Contract", "client", message, request.user)
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
            if client_to_create_contract.status != "ACTUAL":
                message = "You can only create contract to a ACTUAL client"
                make_log("POST", "Contract", "client", message, request.user)
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
            if serializer.validated_data["is_signed"] is True:
                message = "You have to create a not signed contract before to sign it"
                make_log("POST", "Contract", "is_signed", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            if serializer.validated_data["amount"] <= 0:
                message = "Amount have to be positive"
                make_log("POST", "Contract", "amount", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            for data in serializer.validated_data:
                if (
                    data == "payment_due"
                    and serializer.validated_data["payment_due"] < timezone.now()
                ):
                    message = "Payment date have to be superior than the date of today"
                    make_log("POST", "Contract", "payment_due", message, request.user)
                    return Response(
                        {"message": message}, status=status.HTTP_403_FORBIDDEN
                    )

            if Client.objects.filter(
                id=serializer.validated_data["client"].id, contact=request.user.id
            ).exists():
                serializer.save(contact=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return super(ContractViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Contract", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            if instance.is_signed:
                message = "You can't update a signed contract"
                make_log("PUT", "Contract", None, message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            if serializer.validated_data["client"] != instance.client:
                message = "You can't modify the client of a contract"
                make_log("PUT", "Contract", "client", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            if serializer.validated_data["amount"] <= 0:
                message = "Amount have to be positive"
                make_log("PUT", "Contract", "amount", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            for data in serializer.validated_data:
                if (
                    data == "payment_due"
                    and serializer.validated_data["payment_due"] < timezone.now()
                ):
                    message = "Payment date have to be superior than the date of today"
                    make_log("POST", "Contract", "payment_due", message, request.user)
                    return Response(
                        {"message": message}, status=status.HTTP_403_FORBIDDEN
                    )

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
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventViewset(CustomViewset):
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated, HasEventPermission]
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        if self.request.method in ["GET"]:
            return Event.objects.filter(contact=self.request.user.pk)
        return Event.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            for key in serializer.errors.items():
                for k in key[1]:
                    make_log("PUT", "Event", key[0], k, request.user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if instance.is_finished:
            message = "You can't update a finished event"
            make_log("PUT", "Event", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            if serializer.validated_data["contract"] != instance.contract:
                message = "You can't modify the contract of an event"
                make_log("PUT", "Event", "contract", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            if serializer.validated_data["attendees"] <= 0:
                message = "Attendees have to be positive"
                make_log("PUT", "Event", "attendees", message, request.user)
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

            for data in serializer.validated_data:
                if (
                    data == "date"
                    and serializer.validated_data["date"] < timezone.now()
                ):
                    message = "Event date have to be superior than the date of today"
                    make_log("POST", "Event", "date", message, request.user)
                    return Response(
                        {"message": message}, status=status.HTTP_403_FORBIDDEN
                    )
            return super(EventViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_finished:
            message = "You can't delete a finished event"
            make_log("DELETE", "Event", None, message, request.user)
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
