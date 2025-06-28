from django.urls import path
from .views import ProduitListAPI, ProduitDetailAPI, ProduitCategoriesAPI

app_name = 'produits'

urlpatterns = [
    path('api/v1/products/', ProduitListAPI.as_view(), name='produit-list'),
    path('api/v1/products/<uuid:produit_id>/', ProduitDetailAPI.as_view(), name='produit-detail'),
    path('api/v1/products/categories/', ProduitCategoriesAPI.as_view(), name='produit-categories'),
] 