# LOG430 – Laboratoire 4 : Observabilité, Scalabilité et Optimisation

## Présentation
Ce laboratoire vise à transformer une application multi-magasins Django en un système **observable, scalable et robuste**. L'objectif est d'instrumenter l'application, d'identifier les goulets d'étranglement sous charge, puis d'optimiser l'architecture avec un load balancer (NGINX) et un cache Redis.

## Architecture globale
- **Backend** : Django 4.x + Django REST Framework
- **Base de données** : PostgreSQL
- **Load Balancer** : NGINX (scalabilité horizontale)
- **Cache** : Redis (backend Django)
- **Observabilité** : Prometheus (scraping métriques), Grafana (visualisation), logging structuré JSON
- **Tests de charge** : k6 (scripts JS)

## Démarche et étapes réalisées
1. **Observabilité & base de référence**
   - Intégration Prometheus, Grafana, logging JSON, métriques personnalisées
   - Tests de charge avec k6, analyse des goulets d'étranglement
2. **Scalabilité horizontale**
   - Ajout d'un load balancer NGINX, scaling à 3 instances Django
   - Tests de charge "après" load balancer, analyse comparative
3. **Cache Redis**
   - Ajout du service Redis, configuration du cache dans Django
   - Mise en cache des endpoints GET critiques (rapports, stock, indicateurs)
   - Nouveau test de charge, analyse comparative avant/après cache

## Résultats clés
| Test                        | Latence p95 | Taux d'erreur | Débit max (req/s) |
|-----------------------------|-------------|---------------|-------------------|
| Avant LB, 1 instance        | 11s         | 19.7%         | 30                |
| Après LB, 3 instances       | 6.7s        | 19%           | 37                |
| Après cache Redis           | 4.99s       | 10.95%        | 100 (moy) / 1 000+ (pic) |

- **Latence p95** divisée par 2 à 3 selon les endpoints
- **Débit maximal** multiplié par 3 à 30 (pic > 1 000 req/s observé)
- **Taux d'erreur** divisé par deux après cache Redis
- **Stabilité** : plus d'effondrement sous forte charge, saturation absorbée

Pour l'analyse détaillée, voir [`docs/LABO4_OBSERVABILITE.md`](docs/LABO4_OBSERVABILITE.md).

## Utilisation rapide
### Prérequis
- Docker et Docker Compose installés
- Ports 80, 5432, 6379, 9090, 3000 disponibles

### Lancement de l'application et de l'observabilité
```bash
git clone https://github.com/TalipKoyluoglu/LOG430-LabO4
cd LOG430-Labo4
docker-compose up --build --scale app=3 -d
```

### Accès aux outils
- **API Documentation (Swagger)** : http://localhost:8000/swagger/
- **Interface Web** : http://localhost:8000/
- **Prometheus** : http://localhost:9090
- **Grafana** : http://localhost:3000 (admin/admin)

### Lancer un test de charge
```bash
k6 run scripts/stress_test.js
```

## Structure du projet
```plaintext
LOG430-Labo4/
├── config/           # Config Django, Prometheus, Grafana, NGINX
├── magasin/          # App principale (API, services, modèles, vues)
├── scripts/          # Scripts de test de charge (k6)
├── results/          # Résultats des tests (JSON, CSV)
├── docs/             # Documentation, captures d'écran
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Fonctionnalités principales
- **API REST complète** (gestion produits, stocks, ventes, réapprovisionnement)
- **Interface Web Django** (rapports, stock, dashboard, produits)
- **Observabilité avancée** (métriques Prometheus, logs JSON, dashboards Grafana)
- **Scalabilité horizontale** (NGINX + multi-instances)
- **Cache Redis** (optimisation des endpoints GET critiques)
- **Tests de charge automatisés** (k6)

## Tests et développement
- **Tests unitaires, intégration, API** :
  ```bash
  docker-compose run --rm app pytest
  ```
- **Ajout d'un nouvel endpoint** :
  1. Service dans `magasin/services/`
  2. Contrôleur dans `magasin/api/controllers/`
  3. Sérialiseur dans `magasin/api/serializers/`
  4. Route dans `magasin/api/urls.py`
  5. Tests dans `magasin/api/tests/`

## Pipeline CI
- Exemple de pipeline : 

## Auteur
Projet réalisé par Talip Koyluoglu.
