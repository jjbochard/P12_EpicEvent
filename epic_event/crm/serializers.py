from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Client, Contract, Event


class ClientSerializer(ModelSerializer):
    phone_regex = RegexValidator(regex=r"^\+?1?\d{11,11}$")
    fix_phone = serializers.CharField(
        validators=[phone_regex],
        max_length=12,
    )
    mobile_phone = serializers.CharField(
        validators=[phone_regex],
        max_length=12,
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "company",
            "email",
            "fix_phone",
            "mobile_phone",
            "status",
            "contact",
            "date_created",
            "date_updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "contact": {"read_only": True},
            "date_created": {"read_only": True},
            "date_updated": {"read_only": True},
        }


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "is_signed",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
            "contact",
            "client",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "contact": {"read_only": True},
            "date_created": {"read_only": True},
            "date_updated": {"read_only": True},
        }


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "is_finished",
            "attendees",
            "notes",
            "date",
            "date_created",
            "date_updated",
            "contract",
            "contact",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "date_created": {"read_only": True},
            "date_updated": {"read_only": True},
        }
