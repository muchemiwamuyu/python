from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    """
    Generic permission class to restrict access based on user roles.
    Usage: Set `allowed_roles` in the view.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role in self.allowed_roles
        )
