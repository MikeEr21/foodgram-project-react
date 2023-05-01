from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение только для автора и/или админа.
    Остальным только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение только для админов на создание и изменение.
    Остальным только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
