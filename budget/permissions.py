from rest_framework import permissions

class IsBudgetManager(permissions.BasePermission):
    """Permet l'accès uniquement aux gestionnaires de budget."""

    def has_permission(self, request, view):
        # Vérifiez si l'utilisateur a la permission 'budget.manage_budget'
        return request.user.is_authenticated and request.user.has_perm('budget.manage_budget')


class IsFinance(permissions.BasePermission):
    """Permet l'accès uniquement aux utilisateurs du service financier."""

    def has_permission(self, request, view):
        # Vérifiez si l'utilisateur appartient au groupe 'Finance'
        return request.user.is_authenticated and request.user.groups.filter(name='Finance').exists()
