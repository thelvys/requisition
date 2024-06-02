from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'categories', CategoryViewSet)
 

urlpatterns = [
    path('', include(router.urls)),
]
