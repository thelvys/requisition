from rest_framework import viewsets, permissions
from .models import Requisition, Review
from .serializers import RequisitionSerializer, ReviewSerializer
from .permissions import IsRequesterOrReadOnly, IsApprover

class RequisitionViewSet(viewsets.ModelViewSet):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [permissions.IsAuthenticated, IsRequesterOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsApprover]
