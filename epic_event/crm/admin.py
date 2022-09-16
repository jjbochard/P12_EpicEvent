from django.contrib import admin, auth

from .models import Client, Contract, Department, Event, Log


def has_superuser_permission(request):

    return request.user.is_superuser or request.user.is_active and request.user.is_staff


admin.site.has_permission = has_superuser_permission


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "company",
        "fix_phone",
        "mobile_phone",
        "status",
        "contact",
        "date_created",
        "date_updated",
    )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_signed",
        "amount",
        "payment_due",
        "contact",
        "client",
        "date_created",
        "date_updated",
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_finished",
        "attendees",
        "notes",
        "date",
        "contract",
        "contact",
        "date_created",
        "date_updated",
    )


class LogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "model",
        "field",
        "message",
        "user",
        "date",
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Log, LogAdmin)
admin.site.unregister(auth.models.Group)
