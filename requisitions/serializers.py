from rest_framework import serializers
from .models import Requisition, Review, RequisitionShare


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()
    requisition = serializers.PrimaryKeyRelatedField(read_only=True)  # Empêche la modification de la requisition liée

    class Meta:
        model = Review
        fields = '__all__'


class RequisitionShareSerializer(serializers.ModelSerializer):
    shared_with = serializers.StringRelatedField()

    class Meta:
        model = RequisitionShare
        fields = '__all__'


class RequisitionSerializer(serializers.ModelSerializer):
    requester = serializers.StringRelatedField()
    cost_center = serializers.StringRelatedField()
    reviews = ReviewSerializer(many=True, read_only=True)  # Inclure les reviews liées
    shares = RequisitionShareSerializer(many=True, read_only=True)

    class Meta:
        model = Requisition
        fields = '__all__'


