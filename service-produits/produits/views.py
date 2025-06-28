from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .models import Produit
from .serializers import ProduitSerializer, ProduitUpdateSerializer
from .services import (
    get_produit, get_all_produits, create_produit, modifier_produit,
    delete_produit, get_produits_by_categorie, search_produits
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProduitListAPI(ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    @swagger_auto_schema(
        operation_summary="Liste des produits",
        operation_description="Retourne la liste de tous les produits disponibles",
        tags=["Produits"],
        manual_parameters=[
            openapi.Parameter(
                "categorie",
                openapi.IN_QUERY,
                description="Filtrer par catégorie",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Rechercher par nom ou description",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        # Filtrage par catégorie
        categorie = request.query_params.get('categorie')
        if categorie:
            self.queryset = get_produits_by_categorie(categorie)
        
        # Recherche par nom ou description
        search_query = request.query_params.get('search')
        if search_query:
            self.queryset = search_produits(search_query)
        
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Créer un nouveau produit",
        operation_description="Crée un nouveau produit dans le système",
        tags=["Produits"],
        request_body=ProduitSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = ProduitSerializer(data=request.data)
        if serializer.is_valid():
            produit = create_produit(
                nom=serializer.validated_data['nom'],
                categorie=serializer.validated_data['categorie'],
                prix=serializer.validated_data['prix'],
                description=serializer.validated_data.get('description', ''),
                quantite_stock=serializer.validated_data.get('quantite_stock', 0)
            )
            if produit:
                return Response(ProduitSerializer(produit).data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Erreur lors de la création du produit"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProduitDetailAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Détails d'un produit",
        operation_description="Retourne les détails d'un produit par son ID",
        tags=["Produits"],
        manual_parameters=[
            openapi.Parameter(
                "produit_id",
                openapi.IN_PATH,
                description="UUID du produit",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def get(self, request, produit_id):
        produit = get_produit(produit_id)
        if produit:
            serializer = ProduitSerializer(produit)
            return Response(serializer.data)
        else:
            return Response(
                {
                    "error": "Produit non trouvé",
                    "message": f"Produit avec ID {produit_id} introuvable."
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="Mettre à jour un produit",
        operation_description="Modifie les informations d'un produit",
        tags=["Produits"],
        request_body=ProduitUpdateSerializer,
    )
    def put(self, request, produit_id):
        serializer = ProduitUpdateSerializer(data=request.data)
        if serializer.is_valid():
            produit = modifier_produit(produit_id, serializer.validated_data)
            if produit:
                return Response(ProduitSerializer(produit).data)
            else:
                return Response(
                    {
                        "error": "Produit non trouvé",
                        "message": f"Produit avec ID {produit_id} introuvable."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Supprimer un produit",
        operation_description="Supprime un produit du système",
        tags=["Produits"],
    )
    def delete(self, request, produit_id):
        if delete_produit(produit_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "error": "Produit non trouvé",
                    "message": f"Produit avec ID {produit_id} introuvable."
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ProduitCategoriesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Liste des catégories",
        operation_description="Retourne la liste de toutes les catégories de produits",
        tags=["Produits"],
    )
    def get(self, request):
        categories = Produit.objects.values_list('categorie', flat=True).distinct()
        return Response({
            "categories": list(categories),
            "count": len(categories)
        })
