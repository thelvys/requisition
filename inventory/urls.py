from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'items', ItemViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'stock-transfers', StockTransferViewSet)
router.register(r'carriers', CarrierViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'shipments', ShipmentViewSet)
router.register(r'shipment-items', ShipmentItemViewSet)
router.register(r'shipment-status-updates', ShipmentStatusUpdateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
