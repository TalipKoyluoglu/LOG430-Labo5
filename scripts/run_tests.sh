#!/bin/bash

# Script pour lancer les tests de charge du Labo 4
# Usage: ./scripts/run_tests.sh [baseline|stress|both]

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8000"
RESULTS_DIR="results"
SCRIPTS_DIR="scripts"

# Fonction d'affichage
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_prerequisites() {
    print_header "Vérification des prérequis"
    
    # Vérifier que k6 est installé
    if ! command -v k6 &> /dev/null; then
        print_error "k6 n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    print_info "k6 est installé: $(k6 version)"
    
    # Vérifier que l'application Django fonctionne
    if ! curl -s "$BASE_URL/api/v1/reports/" > /dev/null; then
        print_error "L'application Django n'est pas accessible sur $BASE_URL"
        print_warning "Assurez-vous que le serveur Django est démarré: python manage.py runserver"
        exit 1
    fi
    print_info "Application Django accessible sur $BASE_URL"
    
    # Créer le dossier results s'il n'existe pas
    mkdir -p "$RESULTS_DIR"
    print_info "Dossier results créé/vérifié"
}

# Test de base
run_baseline_test() {
    print_header "Lancement du test de base"
    print_info "Ce test simule une charge normale avec montée progressive"
    
    k6 run \
        --out json="$RESULTS_DIR/baseline_test_results.json" \
        --out csv="$RESULTS_DIR/baseline_test_results.csv" \
        "$SCRIPTS_DIR/load_test_baseline.js"
    
    print_info "Test de base terminé. Résultats sauvegardés dans $RESULTS_DIR/"
}

# Test de stress
run_stress_test() {
    print_header "Lancement du test de stress"
    print_warning "Ce test va pousser l'application jusqu'à ses limites"
    print_info "Appuyez sur Ctrl+C pour arrêter le test si nécessaire"
    
    k6 run \
        --out json="$RESULTS_DIR/stress_test_results.json" \
        --out csv="$RESULTS_DIR/stress_test_results.csv" \
        "$SCRIPTS_DIR/stress_test.js"
    
    print_info "Test de stress terminé. Résultats sauvegardés dans $RESULTS_DIR/"
}

# Test rapide pour vérification
run_quick_test() {
    print_header "Test rapide de vérification"
    print_info "Test de 1 minute avec 5 utilisateurs virtuels"
    
    k6 run \
        --duration 1m \
        --vus 5 \
        --out json="$RESULTS_DIR/quick_test_results.json" \
        "$SCRIPTS_DIR/load_test_baseline.js"
    
    print_info "Test rapide terminé"
}

# Affichage des résultats
show_results() {
    print_header "Résultats des tests"
    
    if [ -f "$RESULTS_DIR/baseline_test_results.json" ]; then
        print_info "Test de base: $RESULTS_DIR/baseline_test_results.json"
    fi
    
    if [ -f "$RESULTS_DIR/stress_test_results.json" ]; then
        print_info "Test de stress: $RESULTS_DIR/stress_test_results.json"
    fi
    
    if [ -f "$RESULTS_DIR/quick_test_results.json" ]; then
        print_info "Test rapide: $RESULTS_DIR/quick_test_results.json"
    fi
}

# Menu principal
main() {
    case "${1:-help}" in
        "baseline")
            check_prerequisites
            run_baseline_test
            show_results
            ;;
        "stress")
            check_prerequisites
            run_stress_test
            show_results
            ;;
        "both")
            check_prerequisites
            run_baseline_test
            echo ""
            run_stress_test
            show_results
            ;;
        "quick")
            check_prerequisites
            run_quick_test
            show_results
            ;;
        "help"|*)
            echo "Usage: $0 [baseline|stress|both|quick|help]"
            echo ""
            echo "Options:"
            echo "  baseline  - Test de charge de base (montée progressive)"
            echo "  stress    - Test de stress (jusqu'à l'effondrement)"
            echo "  both      - Lance les deux tests"
            echo "  quick     - Test rapide de vérification (1 min, 5 VUs)"
            echo "  help      - Affiche cette aide"
            echo ""
            echo "Exemples:"
            echo "  $0 baseline    # Test de base seulement"
            echo "  $0 stress      # Test de stress seulement"
            echo "  $0 both        # Les deux tests"
            echo "  $0 quick       # Test rapide"
            ;;
    esac
}

# Exécution
main "$@" 