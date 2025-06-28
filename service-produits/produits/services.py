from .models import Produit
import uuid


def get_produit(produit_id):
    """
    Récupère un produit par son ID
    """
    try:
        return Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return None


def get_all_produits():
    """
    Récupère tous les produits
    """
    return Produit.objects.all()


def create_produit(nom, categorie, prix, description="", quantite_stock=0):
    """
    Crée un nouveau produit
    """
    try:
        produit = Produit.objects.create(
            nom=nom,
            categorie=categorie,
            prix=prix,
            description=description,
            quantite_stock=quantite_stock
        )
        return produit
    except Exception as e:
        print(f"[ERREUR] Création du produit échouée : {e}")
        return None


def modifier_produit(produit_id, data):
    """
    Modifie un produit existant
    """
    try:
        produit = Produit.objects.get(id=produit_id)
        
        # Mise à jour des champs fournis
        if 'nom' in data:
            produit.nom = data['nom']
        if 'categorie' in data:
            produit.categorie = data['categorie']
        if 'prix' in data:
            produit.prix = data['prix']
        if 'description' in data:
            produit.description = data['description']
        if 'quantite_stock' in data:
            produit.quantite_stock = data['quantite_stock']
            
        produit.save()
        return produit
    except Produit.DoesNotExist:
        return None
    except Exception as e:
        print(f"[ERREUR] Modification du produit échouée : {e}")
        return None


def delete_produit(produit_id):
    """
    Supprime un produit
    """
    try:
        produit = Produit.objects.get(id=produit_id)
        produit.delete()
        return True
    except Produit.DoesNotExist:
        return False
    except Exception as e:
        print(f"[ERREUR] Suppression du produit échouée : {e}")
        return False


def get_produits_by_categorie(categorie):
    """
    Récupère tous les produits d'une catégorie
    """
    return Produit.objects.filter(categorie=categorie)


def search_produits(query):
    """
    Recherche des produits par nom ou description
    """
    return Produit.objects.filter(
        nom__icontains=query
    ) | Produit.objects.filter(
        description__icontains=query
    ) 