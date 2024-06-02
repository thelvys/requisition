from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
from .permissions import IsWarehouseManager, IsCarrier

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsWarehouseManager]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [permissions.IsAuthenticated, IsWarehouseManager]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CarrierViewSet(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [permissions.IsAuthenticated, IsCarrier]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCarrier]

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShipmentItemViewSet(viewsets.ModelViewSet):
    queryset = ShipmentItem.objects.all()
    serializer_class = ShipmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShipmentStatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = ShipmentStatusUpdate.objects.all()
    serializer_class = ShipmentStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCarrier]


class StockThresholdViewSet(viewsets.ModelViewSet):
    queryset = StockThreshold.objects.all()
    serializer_class = StockThresholdSerializer
    permission_classes = [permissions.IsAuthenticated, IsWarehouseManager]  # Ou une autre permission appropriée