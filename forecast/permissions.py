from rest_framework import permissions

class IsFinance(permissions.BasePermission):
    """Permet l'accès uniquement aux utilisateurs du service financier."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Finance').exists()
