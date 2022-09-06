from rest_framework.permissions import BasePermission


class HasClientPermission(BasePermission):
    def has_permission(self, request, view):
        print("ok")
        if request.method in ["POST", "PUT", "DELETE"]:
            return bool(
                request.user.department and request.user.department.name == "Sales"
            )
        if request.method == "GET":
            return bool(
                request.user.department
                and request.user.department.name in ["Sales", "Support"]
            )
        return False

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
        if request.method in ["GET", "PUT", "DELETE"]:
            return bool(
                request.user.department and request.user.department.name == "Support"
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PUT", "DELETE"]:
            return bool(obj.contact.pk and obj.contact.pk == request.user.pk)
        return False
