from rest_framework.permissions import BasePermission

from crm.utils import make_log


class HasClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE"]:
            if request.user.department and request.user.department.name == "Sales":
                return True
            make_log(
                request.method,
                "Client",
                None,
                message="You do not have permission to perform this action.",
                user=request.user,
            )

        if request.method == "GET":
            if request.user.department and request.user.department.name in [
                "Sales",
                "Support",
            ]:
                return True
            make_log(
                request.method,
                "Client",
                None,
                message="You do not have permission to perform this action.",
                user=request.user,
            )

        return False

    def has_object_permission(self, request, view, obj):
        return bool(obj.contact.pk and obj.contact.pk == request.user.pk)


class HasContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.department and request.user.department.name == "Sales":
            return True
        make_log(
            request.method,
            "Contract",
            None,
            message="You do not have permission to perform this action.",
            user=request.user,
        )
        return False

    def has_object_permission(self, request, view, obj):
        return bool(obj.contact.pk and obj.contact.pk == request.user.pk)


class HasEventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "DELETE"]:
            if request.user.department and request.user.department.name == "Sales":
                return True
            make_log(
                request.method,
                "Event",
                None,
                message="You do not have permission to perform this action.",
                user=request.user,
            )

        if request.method in ["GET", "PUT"]:
            if request.user.department and request.user.department.name == "Support":
                return True
            make_log(
                request.method,
                "Event",
                None,
                message="You do not have permission to perform this action.",
                user=request.user,
            )

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PUT", "DELETE"]:
            return bool(obj.contact.pk and obj.contact.pk == request.user.pk)
        return False
