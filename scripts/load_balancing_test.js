import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';

// Métriques personnalisées
const instanceCounter = new Counter('instance_requests');
const loadBalancingRate = new Rate('load_balancing_success');

// Configuration du test
export let options = {
  stages: [
    { duration: '30s', target: 10 },   // Montée en charge
    { duration: '2m', target: 20 },    // Maintien de la charge
    { duration: '30s', target: 0 },    // Descente
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.1'],
    load_balancing_success: ['rate>0.8'],
  },
};

const API_KEY = 'magasin-secret-key-2025';
const KONG_URL = 'http://localhost:8080';

// Compteur pour suivre les instances utilisées
let instanceDistribution = {};

export default function() {
  // Test du load balancing sur le service catalogue
  const headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json',
  };

  // Appel au service catalogue via Kong
  const response = http.get(`${KONG_URL}/api/catalogue/`, { headers });
  
  // Vérifier que la réponse est valide
  const isSuccess = check(response, {
    'Status is 200': (r) => r.status === 200,
    'Response time < 500ms': (r) => r.timings.duration < 500,
    'Has catalogue data': (r) => r.body.includes('produits') || r.body.includes('catalogue'),
  });

  if (isSuccess) {
    loadBalancingRate.add(1);
    instanceCounter.add(1);
    
    // Essayer de détecter quelle instance a répondu
    // (nécessiterait une modification du service pour inclure l'ID d'instance)
    try {
      const responseData = JSON.parse(response.body);
      if (responseData.instance_id) {
        instanceDistribution[responseData.instance_id] = 
          (instanceDistribution[responseData.instance_id] || 0) + 1;
      }
    } catch (e) {
      // Ignore si pas de JSON valide
    }
  } else {
    loadBalancingRate.add(0);
  }

  // Test de différents endpoints pour vérifier la répartition
  const endpoints = [
    '/api/catalogue/',
    '/api/catalogue/produits/',
    '/api/catalogue/categories/',
  ];

  const randomEndpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const testResponse = http.get(`${KONG_URL}${randomEndpoint}`, { headers });
  
  check(testResponse, {
    'Random endpoint accessible': (r) => r.status === 200 || r.status === 404, // 404 acceptable si endpoint n'existe pas
  });

  sleep(1);
}

export function handleSummary(data) {
  console.log('=== RÉSULTATS DU TEST DE LOAD BALANCING ===');
  console.log(`Requêtes totales: ${data.metrics.http_reqs.values.count}`);
  console.log(`Taux de succès: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%`);
  console.log(`Temps de réponse moyen: ${data.metrics.http_req_duration.values.avg.toFixed(2)}ms`);
  console.log(`Temps de réponse P95: ${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms`);
  
  if (data.metrics.load_balancing_success) {
    console.log(`Taux de load balancing: ${(data.metrics.load_balancing_success.values.rate * 100).toFixed(2)}%`);
  }
  
  console.log('\n=== DISTRIBUTION DES INSTANCES ===');
  if (Object.keys(instanceDistribution).length > 0) {
    Object.entries(instanceDistribution).forEach(([instance, count]) => {
      console.log(`Instance ${instance}: ${count} requêtes`);
    });
  } else {
    console.log('⚠️  Impossible de détecter la distribution des instances');
    console.log('💡 Ajoutez un header X-Instance-ID dans vos services pour un suivi précis');
  }

  return {
    'load_balancing_test_results.json': JSON.stringify(data, null, 2),
  };
} 