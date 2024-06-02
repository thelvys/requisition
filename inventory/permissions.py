from rest_framework import permissions

class IsWarehouseManager(permissions.BasePermission):
    """Permet l'accès uniquement aux responsables d'entrepôt."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Autoriser la lecture à tous
            return True
        return obj.warehouse.manager == request.user


class IsCarrier(permissions.BasePermission):
    """Permet l'accès uniquement aux transporteurs."""

    # Implémentez la logique de vérification ici (par exemple, en vérifiant un champ 'is_carrier' sur l'utilisateur)
    pass
