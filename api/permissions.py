from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyPermission(BasePermission):
    """Класс для разрешения доступа только для чтения."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AdminPermission(BasePermission):
    """Класс для разрешения доступа только администратору."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_superuser
            )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.role == request.user.is_staff
            or request.user.is_superuser
        )
