from django.urls import path
from .views import StockCentralListAPI, StockLocalListAPI, DemandeReapprovisionnementCreateAPI

app_name = 'stock'

urlpatterns = [
    path('api/v1/stock/central/', StockCentralListAPI.as_view(), name='stock-central-list'),
    path('api/v1/stock/local/<uuid:magasin_id>/', StockLocalListAPI.as_view(), name='stock-local-list'),
    path('api/v1/stock/reapprovisionnement/', DemandeReapprovisionnementCreateAPI.as_view(), name='demande-reapprovisionnement-create'),
] 