from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CashFlowForecastViewSet, ForecastItemViewSet

router = DefaultRouter()
router.register(r'forecasts', CashFlowForecastViewSet)
router.register(r'forecast-items', ForecastItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
