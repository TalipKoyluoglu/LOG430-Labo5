import requests

class UC2_StockControleur:
    BASE_URL = "http://stock-service:8000/api/v1/stock/"
    # En local, utiliser : "http://localhost:8002/api/v1/stock/"

    def obtenir_stock_central(self):
        url = f"{self.BASE_URL}central/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []

    def obtenir_stock_local(self, magasin_id):
        url = f"{self.BASE_URL}local/{magasin_id}/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []

    def creer_demande_reapprovisionnement(self, produit_id, magasin_id, quantite):
        url = f"{self.BASE_URL}reapprovisionnement/"
        data = {
            "produit_id": produit_id,
            "magasin_id": magasin_id,
            "quantite": quantite
        }
        try:
            response = requests.post(url, json=data, timeout=3)
            if response.status_code == 201:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None
