from rest_framework import viewsets, permissions
from .models import Budget, BudgetItem, BudgetPeriod, RequisitionBudget
from .serializers import BudgetSerializer, BudgetItemSerializer, BudgetPeriodSerializer, RequisitionBudgetSerializer
from .permissions import IsBudgetManager, IsFinance  # Permissions personnalisées

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsBudgetManager]  # Permission pour les gestionnaires de budget


class BudgetItemViewSet(viewsets.ModelViewSet):
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsBudgetManager]


class BudgetPeriodViewSet(viewsets.ModelViewSet):
    queryset = BudgetPeriod.objects.all()
    serializer_class = BudgetPeriodSerializer
    permission_classes = [permissions.IsAuthenticated, IsFinance]  # Permission pour le service financier


class RequisitionBudgetViewSet(viewsets.ModelViewSet):
    queryset = RequisitionBudget.objects.all()
    serializer_class = RequisitionBudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsBudgetManager]  # Ou une permission plus spécifique