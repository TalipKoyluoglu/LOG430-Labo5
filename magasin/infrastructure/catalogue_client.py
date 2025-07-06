"""
Client HTTP pour le Service Catalogue via Kong API Gateway
Communication avec les endpoints DDD du service-catalogue
"""
import requests
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

BASE_URL = "http://log430-labo5-kong-1:8000/api/catalogue"

class CatalogueClient:
    """
    Client HTTP pour communiquer avec le service-catalogue
    Encapsule tous les appels REST vers les endpoints DDD
    """
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Key': 'magasin-secret-key-2025'  # Clé API Kong
        })
    
    def health_check(self) -> Dict[str, Any]:
        """
        GET /api/ddd/catalogue/health-check/
        Vérification de l'état du service catalogue
        """
        try:
            response = self.session.get(f"{self.base_url}/api/ddd/catalogue/health-check/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur health check catalogue: {e}")
            return {"status": "error", "message": str(e)}
    
    def rechercher_produits(self, 
                          nom: Optional[str] = None,
                          categorie_id: Optional[str] = None, 
                          prix_min: Optional[float] = None,
                          prix_max: Optional[float] = None,
                          actifs_seulement: bool = True,
                          criteres: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GET /api/ddd/catalogue/rechercher/
        Use Case: RechercherProduitsUseCase
        """
        try:
            params = {}
            
            # Si des critères sont fournis, les utiliser
            if criteres:
                params.update(criteres)
            else:
                # Sinon, utiliser les paramètres individuels
                if nom:
                    params['nom'] = nom
                if categorie_id:
                    params['categorie_id'] = categorie_id
                if prix_min is not None:
                    params['prix_min'] = prix_min
                if prix_max is not None:
                    params['prix_max'] = prix_max
                if actifs_seulement is not None:
                    params['actifs_seulement'] = actifs_seulement
            
            response = self.session.get(
                f"{self.base_url}/api/ddd/catalogue/rechercher/",
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur recherche produits: {e}")
            return {
                'success': False,
                'error': f'Erreur de communication avec le service catalogue: {str(e)}',
                'data': {'produits': [], 'total': 0}
            }
    
    def ajouter_produit(self, nom: str, categorie: str, prix: float, description: str = "") -> Dict[str, Any]:
        """
        POST /api/ddd/catalogue/ajouter/
        Use Case: AjouterProduitUseCase
        """
        try:
            data = {
                'nom': nom,
                'categorie': categorie,
                'prix': prix,
                'description': description
            }
            
            response = self.session.post(
                f"{self.base_url}/api/ddd/catalogue/ajouter/",
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur ajout produit: {e}")
            return {
                'success': False,
                'error': f'Erreur lors de l\'ajout du produit: {str(e)}'
            }
    
    def obtenir_produit_par_id(self, produit_id: str) -> Dict[str, Any]:
        """
        GET /api/ddd/catalogue/produits/<uuid>/
        Récupère les détails d'un produit spécifique par son ID
        """
        try:
            response = self.session.get(f"{self.base_url}/api/ddd/catalogue/produits/{produit_id}/")
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur récupération produit {produit_id}: {e}")
            return {
                'success': False,
                'error': f'Produit {produit_id} non trouvé: {str(e)}'
            }
    
    def obtenir_tous_produits(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les produits actifs
        """
        try:
            resultat = self.rechercher_produits(actifs_seulement=True)
            if resultat.get('success', False):
                return resultat.get('data', {}).get('produits', [])
            else:
                logger.warning(f"Échec récupération tous produits: {resultat.get('error', 'Erreur inconnue')}")
                return []
                
        except Exception as e:
            logger.error(f"Erreur récupération tous produits: {e}")
            return []
