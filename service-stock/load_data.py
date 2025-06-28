#!/usr/bin/env python
"""
Script pour charger les données initiales dans le service-stock
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stock.models import StockCentral, StockLocal
import json


def load_initial_data():
    """Charge les données initiales depuis le fichier JSON"""
    try:
        with open('initial_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            if item['model'] == 'stock.stockcentral':
                fields = item['fields']
                stock_id = item['pk']
                if not StockCentral.objects.filter(id=stock_id).exists():
                    StockCentral.objects.create(
                        id=stock_id,
                        produit_id=fields['produit_id'],
                        quantite=fields['quantite']
                    )
                    print(f"✅ StockCentral créé : {fields['produit_id']} ({fields['quantite']})")
                else:
                    print(f"⏭️  StockCentral déjà existant : {fields['produit_id']}")
            elif item['model'] == 'stock.stocklocal':
                fields = item['fields']
                stock_id = item['pk']
                if not StockLocal.objects.filter(id=stock_id).exists():
                    StockLocal.objects.create(
                        id=stock_id,
                        produit_id=fields['produit_id'],
                        magasin_id=fields['magasin_id'],
                        quantite=fields['quantite']
                    )
                    print(f"✅ StockLocal créé : {fields['produit_id']} - {fields['magasin_id']} ({fields['quantite']})")
                else:
                    print(f"⏭️  StockLocal déjà existant : {fields['produit_id']} - {fields['magasin_id']}")
        
        print(f"\n🎉 Chargement terminé ! {StockCentral.objects.count()} StockCentral, {StockLocal.objects.count()} StockLocal dans la base.")
        
    except FileNotFoundError:
        print("❌ Fichier initial_data.json non trouvé")
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")


if __name__ == '__main__':
    load_initial_data() 