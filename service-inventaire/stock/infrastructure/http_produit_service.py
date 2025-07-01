"""
Implémentation HTTP du service Produit
Communique avec le service-catalogue via HTTP pour valider les produits.
"""
import requests
from typing import Optional

from ..application.services.produit_service import ProduitService
from ..domain.value_objects import ProduitId
from ..domain.exceptions import ProduitInexistantError


class HttpProduitService(ProduitService):
    """Implémentation concrète du service Produit utilisant HTTP"""
    
    def __init__(self, catalogue_base_url: str = "http://catalogue-service:8000"):
        self.catalogue_base_url = catalogue_base_url.rstrip('/')
    
    def produit_existe(self, produit_id: ProduitId) -> bool:
        """Vérifie si un produit existe dans le service catalogue"""
        try:
            response = requests.get(
                f"{self.catalogue_base_url}/api/ddd/catalogue/produits/{produit_id}/",
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            # En cas d'erreur réseau, on assume que le produit n'existe pas
            return False
    
    def valider_produit_existe(self, produit_id: ProduitId) -> None:
        """
        Valide qu'un produit existe, lève une exception sinon
        """
        if not self.produit_existe(produit_id):
            raise ProduitInexistantError(f"Le produit {produit_id} n'existe pas")
    
    def get_nom_produit(self, produit_id: ProduitId) -> str:
        """Récupère le nom d'un produit pour l'affichage"""
        try:
            response = requests.get(
                f"{self.catalogue_base_url}/api/ddd/catalogue/produits/{produit_id}/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('nom', f"Produit {produit_id}")
            else:
                return f"Produit {produit_id}"
        except requests.RequestException:
            return f"Produit {produit_id}" 