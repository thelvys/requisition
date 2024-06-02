from rest_framework import viewsets, permissions
from .models import CashFlowForecast, ForecastItem
from .serializers import CashFlowForecastSerializer, ForecastItemSerializer
from .permissions import IsFinance  # Permission personnalisée

class CashFlowForecastViewSet(viewsets.ModelViewSet):
    queryset = CashFlowForecast.objects.all()
    serializer_class = CashFlowForecastSerializer
    permission_classes = [permissions.IsAuthenticated, IsFinance]  # Seuls les utilisateurs du service financier peuvent gérer les prévisions


class ForecastItemViewSet(viewsets.ModelViewSet):
    queryset = ForecastItem.objects.all()
    serializer_class = ForecastItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsFinance]
