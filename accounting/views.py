from rest_framework import viewsets, permissions
from .models import Account, Period, Journal, Transaction, TransactionItem
from .serializers import *
from .permissions import IsAccountant, IsAccountManager, IsAccountGroupManager

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountGroupManager]


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountGroupManager]


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountGroupManager]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountant | IsAccountManager]  # Les comptables peuvent modifier, les gestionnaires peuvent lire


class TransactionItemViewSet(viewsets.ModelViewSet):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountant]  # Seuls les comptables peuvent modifier les lignes
