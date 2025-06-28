from rest_framework import serializers
from .models import StockCentral, StockLocal, DemandeReapprovisionnement

class StockCentralSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCentral
        fields = ['id', 'produit_id', 'quantite', 'created_at', 'updated_at']

class StockLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLocal
        fields = ['id', 'produit_id', 'magasin_id', 'quantite', 'created_at', 'updated_at']

class DemandeReapprovisionnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeReapprovisionnement
        fields = ['id', 'produit_id', 'magasin_id', 'quantite', 'date', 'statut'] 