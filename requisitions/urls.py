from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequisitionViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'requisitions', RequisitionViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
