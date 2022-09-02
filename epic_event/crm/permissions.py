from rest_framework.permissions import BasePermission


class HasClientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.department and request.user.department.name == "Sales")

    def has_object_permission(self, request, view, obj):
        return bool(obj.contact.pk and obj.contact.pk == request.user.pk)


class HasContractPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.department and request.user.department.name == "Sales")

    def has_object_permission(self, request, view, obj):
        return bool(obj.contact.pk and obj.contact.pk == request.user.pk)


class HasEventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user.department and request.user.department.name == "Sales"
            )
        elif request.method == "GET":
            return bool(
                request.user.department and request.user.department.name == "Support"
            )

    def has_object_permission(self, request, view, obj):
        return bool(obj.contact.pk and obj.contact.pk == request.user.pk)
