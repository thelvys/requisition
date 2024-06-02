from rest_framework import serializers
from requisitions.serializers import RequisitionSerializer
from .models import Budget, BudgetItem, BudgetPeriod, RequisitionBudget, Expense
from groups.serializers import DepartmentSerializer, CategorySerializer  # Assurez-vous d'avoir des sérialiseurs pour Department et Category


class BudgetPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPeriod
        fields = '__all__'


class BudgetItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = BudgetItem
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    cost_center = DepartmentSerializer()
    period = BudgetPeriodSerializer()
    items = BudgetItemSerializer(many=True, read_only=True)  # Inclure les lignes budgétaires liées

    class Meta:
        model = Budget
        fields = '__all__'

class RequisitionBudgetSerializer(serializers.ModelSerializer):
    requisition = RequisitionSerializer()
    budget_item = BudgetItemSerializer()

    class Meta:
        model = RequisitionBudget
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    requisition = RequisitionSerializer()
    budget_item = BudgetItemSerializer()

    class Meta:
        model = Expense
        fields = '__all__'