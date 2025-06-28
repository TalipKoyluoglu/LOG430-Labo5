from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import StockCentral, StockLocal, DemandeReapprovisionnement
from .serializers import StockCentralSerializer, StockLocalSerializer, DemandeReapprovisionnementSerializer
from .services import obtenir_stock_central, obtenir_stock_magasin, creer_demande_reapprovisionnement
import requests

# Create your views here.

class StockCentralListAPI(ListAPIView):
    queryset = StockCentral.objects.all()
    serializer_class = StockCentralSerializer

class StockLocalListAPI(APIView):
    def get(self, request, magasin_id):
        stock = obtenir_stock_magasin(magasin_id)
        return Response(stock, status=status.HTTP_200_OK)

class DemandeReapprovisionnementCreateAPI(CreateAPIView):
    queryset = DemandeReapprovisionnement.objects.all()
    serializer_class = DemandeReapprovisionnementSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            produit_id = serializer.validated_data['produit_id']
            magasin_id = serializer.validated_data['magasin_id']
            quantite = serializer.validated_data['quantite']

            # Vérification produit via service-produits
            produits_url = f"http://produits-service:8000/api/v1/products/{produit_id}/"
            try:
                produit_response = requests.get(produits_url, timeout=3)
                if produit_response.status_code != 200:
                    return Response(
                        {"error": "Produit inexistant dans le service-produits"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except requests.RequestException:
                return Response(
                    {"error": "Service-produits injoignable"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            # Vérification magasin via service-magasins (à adapter selon ton URL)
            magasins_url = f"http://magasins-service:8000/api/v1/magasins/{magasin_id}/"
            try:
                magasin_response = requests.get(magasins_url, timeout=3)
                if magasin_response.status_code != 200:
                    return Response(
                        {"error": "Magasin inexistant dans le service-magasins"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except requests.RequestException:
                return Response(
                    {"error": "Service-magasins injoignable"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            # Vérification quantité disponible dans le stock central
            try:
                stock_central = StockCentral.objects.get(produit_id=produit_id)
                if stock_central.quantite < quantite:
                    return Response(
                        {"error": "Stock central insuffisant pour ce produit"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except StockCentral.DoesNotExist:
                return Response(
                    {"error": "Aucune entrée de stock central pour ce produit"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            success = creer_demande_reapprovisionnement(produit_id, magasin_id, quantite)
            if success:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Erreur lors de la création de la demande'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
