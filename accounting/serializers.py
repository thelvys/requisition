from rest_framework import serializers
from .models import Account, Period, Journal, Transaction, TransactionItem

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'


class TransactionItemSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()

    class Meta:
        model = TransactionItem
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    journal = serializers.StringRelatedField()
    items = TransactionItemSerializer(many=True, read_only=True)  # Inclure les lignes de transaction liées

    class Meta:
        model = Transaction
        fields = '__all__'
