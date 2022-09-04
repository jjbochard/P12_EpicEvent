from django.contrib import admin, auth

from .models import User


def has_superuser_permission(request):

    return request.user.is_superuser or request.user.is_active and request.user.is_staff


admin.site.has_permission = has_superuser_permission


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )


admin.site.register(User, UserAdmin)
