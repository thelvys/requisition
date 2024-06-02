from rest_framework import viewsets, permissions
from .models import CashAccount, Payment, AccountTransfer, AccountGroup
from .serializers import CashAccountSerializer, PaymentSerializer, AccountTransferSerializer
from .permissions import IsAccountant, IsAccountManager, IsAccountGroupManager  # Permissions personnalisées

class CashAccountViewSet(viewsets.ModelViewSet):
    queryset = CashAccount.objects.all()
    serializer_class = CashAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountManager]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountant]


class AccountTransferViewSet(viewsets.ModelViewSet):
    queryset = AccountTransfer.objects.all()
    serializer_class = AccountTransferSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountant]

class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountGroupManager]
