from django.contrib import admin, auth

from .models import Client, Department


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
    )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.unregister(auth.models.Group)
