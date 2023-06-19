from rest_framework import permissions


class IsOwnerUserOrAdmin(permissions.BasePermission):
    """Checks if the authenticated user is the owner of the object."""

    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user or request.user.is_staff)
