from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'cash-accounts', CashAccountViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'account-transfers', AccountTransferViewSet)
router.register(r'account-groups', AccountGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
