from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from .models import Period

class IsAccountant(permissions.BasePermission):
    """Permet aux comptables de créer des transactions et de modifier/supprimer celles créées dans les dernières 72 heures."""

    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est authentifié et appartient au groupe "Comptable"
        if not request.user.is_authenticated or not request.user.groups.filter(name='Comptable').exists():
            return False

        # Vérifier si une période comptable est ouverte
        active_period = Period.objects.filter(is_closed=False).first()
        if not active_period:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Autoriser la lecture à tous
            return True

        # Autoriser la modification/suppression si la transaction a été créée dans les dernières 72 heures
        return obj.date >= timezone.now() - timedelta(hours=72)


class IsAccountManager(permissions.BasePermission):
    """Permet aux gestionnaires de comptes de visualiser les comptes et les transactions, mais pas de les modifier."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Gestionnaire de compte').exists()

    def has_object_permission(self, request, view, obj):
        # Autorise la lecture, mais pas les autres actions
        return request.method in permissions.SAFE_METHODS


class IsAccountGroupManager(permissions.BasePermission):
    """Permet aux gestionnaires de groupes de comptes de tout faire, y compris attribuer des comptes et définir les périodes."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Gestionnaire de groupe de compte').exists()
