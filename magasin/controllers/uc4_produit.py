import requests

class UC4_ProduitControleur:
    # Utilise le nom du service Docker pour la communication inter-containers
    BASE_URL = "http://catalogue-service:8000/api/v1/products/"
    # En local (hors Docker), utiliser : "http://localhost:8001/api/v1/products/"

    def lister_produits(self):
        url = self.BASE_URL
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []

    def creer_produit(self, nom, categorie, prix, quantite_stock=0, description=""):
        url = self.BASE_URL
        data = {
            "nom": nom,
            "categorie": categorie,
            "prix": prix,
            "quantite_stock": quantite_stock,
            "description": description
        }
        try:
            response = requests.post(url, json=data, timeout=3)
            if response.status_code == 201:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None

    def get_produit(self, produit_id):
        url = f"{self.BASE_URL}{produit_id}/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None

    def modifier_produit(self, produit_id, nom=None, categorie=None, prix=None, quantite_stock=None, description=None):
        url = f"{self.BASE_URL}{produit_id}/"
        data = {}
        if nom is not None:
            data["nom"] = nom
        if categorie is not None:
            data["categorie"] = categorie
        if prix is not None:
            data["prix"] = prix
        if quantite_stock is not None:
            data["quantite_stock"] = quantite_stock
        if description is not None:
            data["description"] = description
        try:
            response = requests.put(url, json=data, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None

    def supprimer_produit(self, produit_id):
        url = f"{self.BASE_URL}{produit_id}/"
        try:
            response = requests.delete(url, timeout=3)
            return response.status_code == 204
        except requests.RequestException:
            return False

    def lister_categories(self):
        url = f"{self.BASE_URL}categories/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []
