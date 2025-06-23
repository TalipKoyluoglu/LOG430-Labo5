from magasin.models import Vente, LigneVente, Magasin, StockLocal
from django.core.cache import cache


def generer_rapport_consolide():
    cache_key = "rapport_consolide"
    data = cache.get(cache_key)
    if data is not None:
        return data
    rapports = []
    magasins = Magasin.objects.all()

    for magasin in magasins:
        ventes = Vente.objects.filter(magasin=magasin)
        total = sum(
            ligne.quantite * ligne.prix_unitaire
            for vente in ventes
            for ligne in vente.lignes.all()
        )

        produits_vendus = {}
        for vente in ventes:
            for ligne in vente.lignes.all():
                nom_produit = ligne.produit.nom
                produits_vendus[nom_produit] = (
                    produits_vendus.get(nom_produit, 0) + ligne.quantite
                )

        stock_local = {
            s.produit.nom: s.quantite
            for s in StockLocal.objects.filter(magasin=magasin)
        }

        rapports.append(
            {
                "magasin": magasin.nom,
                "total": total,
                "produits_vendus": produits_vendus,
                "stock_local": stock_local,
            }
        )
    cache.set(cache_key, rapports, timeout=60)
    return rapports
