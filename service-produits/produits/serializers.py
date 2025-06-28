from rest_framework import serializers
from .models import Produit


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'categorie', 'prix', 'quantite_stock', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProduitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'prix', 'description'] 