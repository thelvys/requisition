from rest_framework import serializers
from .models import StockThreshold, Supplier, Warehouse, Item, Stock, StockTransfer, Carrier, Vehicle, Shipment, ShipmentItem, ShipmentStatusUpdate

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()

    class Meta:
        model = Warehouse
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    item = ItemSerializer()

    class Meta:
        model = Stock
        fields = '__all__'

class StockTransferSerializer(serializers.ModelSerializer):
    from_warehouse = WarehouseSerializer()
    to_warehouse = WarehouseSerializer()
    item = ItemSerializer()
    approved_by = serializers.StringRelatedField()

    class Meta:
        model = StockTransfer
        fields = '__all__'

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    carrier = CarrierSerializer()

    class Meta:
        model = Vehicle
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField()
    warehouse = WarehouseSerializer()
    carrier = CarrierSerializer()
    vehicle = VehicleSerializer()
    status_updates = serializers.StringRelatedField(many=True, read_only=True)
    items = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'

class ShipmentItemSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(read_only=True)
    order_item = serializers.StringRelatedField()

    class Meta:
        model = ShipmentItem
        fields = '__all__'

class ShipmentStatusUpdateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShipmentStatusUpdate
        fields = '__all__'

class StockThresholdSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()  # Affiche le nom de l'article

    class Meta:
        model = StockThreshold
        fields = '__all__'

