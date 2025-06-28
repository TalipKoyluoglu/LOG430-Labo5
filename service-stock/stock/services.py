from .models import StockCentral, StockLocal, DemandeReapprovisionnement


def obtenir_stock_central():
    return list(StockCentral.objects.all())


def creer_demande_reapprovisionnement(produit_id, magasin_id, quantite):
    try:
        DemandeReapprovisionnement.objects.create(
            produit_id=produit_id, magasin_id=magasin_id, quantite=quantite
        )
        return True
    except Exception as e:
        print(f"[ERREUR] Création de la demande échouée : {e}")
        return False


def obtenir_stock_magasin(magasin_id):
    try:
        stock_entries = StockLocal.objects.filter(magasin_id=magasin_id)
    except StockLocal.DoesNotExist:
        return []
    reponse = []
    for stock in stock_entries:
        reponse.append(
            {
                "produit_id": str(stock.produit_id),
                "magasin_id": str(stock.magasin_id),
                "quantite": stock.quantite,
            }
        )
    return reponse 