from rest_framework import permissions

class IsRequesterOrReadOnly(permissions.BasePermission):
    """Permet l'accès en lecture seule à tous, mais l'accès en écriture uniquement au demandeur."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.requester == request.user


class IsApprover(permissions.BasePermission):
    """Permet l'accès uniquement aux utilisateurs ayant la permission d'approuver."""

    def has_permission(self, request, view):
        # Vérifiez si l'utilisateur a la permission 'requisition.approve_requisition'
        return request.user.is_authenticated and request.user.has_perm('requisition.approve_requisition')
