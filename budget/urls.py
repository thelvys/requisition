from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, BudgetItemViewSet, BudgetPeriodViewSet, RequisitionBudgetViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet)
router.register(r'budget-items', BudgetItemViewSet)
router.register(r'budget-periods', BudgetPeriodViewSet)
router.register(r'requisition-budgets', RequisitionBudgetViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
