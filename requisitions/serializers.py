from rest_framework import serializers
from .models import Requisition, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class RequisitionSerializer(serializers.ModelSerializer):
    requester = serializers.StringRelatedField()  # Affiche le nom de l'utilisateur
    cost_center = serializers.StringRelatedField()
    approved_by = serializers.StringRelatedField()
    reviews = ReviewSerializer(many=True, read_only=True)  # Inclure les reviews liées

    class Meta:
        model = Requisition
        fields = '__all__'

