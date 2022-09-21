from django.contrib import admin

from .models import User


def has_superuser_permission(request):

    return request.user.is_superuser or request.user.is_active and request.user.is_staff


admin.site.has_permission = has_superuser_permission


class UserAdmin(admin.ModelAdmin):
    def add_view(self, request, extra_context=None):

        self.exclude = (
            "username",
            "last_login",
            "groups",
            "date_joined",
            "user_permissions",
        )
        return super(UserAdmin, self).change_view(request, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.exclude = (
            "password",
            "last_login",
            "groups",
            "date_joined",
            "user_permissions",
        )
        return super(UserAdmin, self).change_view(request, object_id, extra_context)

    list_display = (
        "id",
        "email",
        "phone",
        "department",
        "date_joined",
        "is_staff",
    )


admin.site.register(User, UserAdmin)
