from rest_framework import serializers
from .models import CashAccount, Payment, AccountTransfer, AccountGroup
from requisition.serializers import RequisitionSerializer  # Importez le sérialiseur de Requisition


class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = '__all__'


class CashAccountSerializer(serializers.ModelSerializer):
    account_group = AccountGroupSerializer()
    assigned_to = serializers.StringRelatedField()

    class Meta:
        model = CashAccount
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    requisition = RequisitionSerializer()  # Utilisez le sérialiseur de Requisition pour les détails
    cash_account = CashAccountSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class AccountTransferSerializer(serializers.ModelSerializer):
    from_account = CashAccountSerializer()
    to_account = CashAccountSerializer()

    class Meta:
        model = AccountTransfer
        fields = '__all__'
