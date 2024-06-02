# groups/serializers.py

from rest_framework import serializers
from .models import Department, Category


class DepartmentSerializer(serializers.ModelSerializer):
    main_dep = serializers.StringRelatedField(allow_null=True)  # Affiche le nom du département parent (ou null si aucun)
    supervisor = serializers.StringRelatedField(allow_null=True)  # Affiche le nom du superviseur (ou null si aucun)

    class Meta:
        model = Department
        fields = '__all__'  # Ou spécifiez les champs que vous voulez exposer


class CategorySerializer(serializers.ModelSerializer):
    main_cat = serializers.StringRelatedField(allow_null=True)  # Affiche le nom de la catégorie parente (ou null si aucune)

    class Meta:
        model = Category
        fields = '__all__'  # Ou spécifiez les champs que vous voulez exposer
