from rest_framework import viewsets, permissions
from .models import Requisition, Review
from .serializers import RequisitionSerializer, ReviewSerializer
from .permissions import IsRequesterOrReadOnly, IsApprover, CanViewSharedRequisition, CanShareRequisition

class RequisitionViewSet(viewsets.ModelViewSet):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [permissions.IsAuthenticated, IsRequesterOrReadOnly | CanViewSharedRequisition, CanShareRequisition]

    def get_queryset(self):
        """Filtre les requisitions pour n'afficher que celles partagées avec l'utilisateur."""
        if self.request.user.has_perm('requisition.approve_requisition'):
            return Requisition.objects.filter(shares__shared_with=self.request.user)
        return Requisition.objects.filter(requester=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsApprover]
