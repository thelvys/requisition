from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'journals', JournalViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transaction-items', TransactionItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
