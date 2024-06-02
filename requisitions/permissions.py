from rest_framework import permissions
from .models import Requisition, Review, RequisitionShare

class IsRequesterOrReadOnly(permissions.BasePermission):
    """Permet l'accès en lecture seule à tous, mais l'accès en écriture uniquement au demandeur."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.requester == request.user


class IsApprover(permissions.BasePermission):
    """Permet l'accès uniquement à l'approbateur désigné pour le niveau actuel."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Autoriser la lecture à tous
            return True

        if isinstance(obj, Requisition):
            # Pour les requisitions, vérifier si l'utilisateur est l'approbateur du niveau suivant
            next_level = obj.reviews.filter(status=Review.REVIEW_PENDING).first()
            return next_level and next_level.reviewer == request.user

        if isinstance(obj, Review):
            # Pour les reviews, vérifier si l'utilisateur est l'approbateur de cette review
            return obj.reviewer == request.user

        return False
    

class CanViewSharedRequisition(permissions.BasePermission):
    """Permet l'accès uniquement aux requisitions partagées avec l'utilisateur et s'il a la permission d'approbateur."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Lecture
            return (
                obj.requester == request.user or
                obj.shares.filter(shared_with=request.user).exists() and request.user.has_perm('requisition.approve_requisition')
            )
        return obj.requester == request.user  # Écriture seulement pour le demandeur


class CanShareRequisition(permissions.BasePermission):
    """Permet de partager une requisition seulement si l'utilisateur est le propriétaire ou a le droit de partager."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Lecture
            return True

        # Autoriser le partage si l'utilisateur est le propriétaire
        if obj.requester == request.user:
            return True

        # Autoriser le partage si la requête a été partagée avec l'utilisateur et qu'il a le droit de partager
        try:
            share = RequisitionShare.objects.get(requisition=obj, shared_with=request.user)
            return share.can_approve  # Vérifier si l'utilisateur a le droit de partager
        except RequisitionShare.DoesNotExist:
            return False