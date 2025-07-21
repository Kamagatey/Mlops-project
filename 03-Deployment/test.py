import requests
import json

# Données de test
data = {
    "posted_speed_limit": 30,
    "weather_condition": "CLEAR",
    "lighting_condition": "DAYLIGHT",
    "first_crash_type": "REAR END",
    "trafficway_type": "ONE-WAY",
    "roadway_surface_cond": "DRY",
    "prim_contributory_cause": "FOLLOWING TOO CLOSELY",
    "crash_hour": 14,
    "delay_police_minutes": 5.0
}

# URL de l'API
url = "http://localhost:8000/predict"

try:
    # Envoi de la requête
    response = requests.post(url, json=data, timeout=10)
    
    # Vérification de la réponse
    if response.status_code == 200:
        print("✅ Requête réussie:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Erreur {response.status_code}:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"🔌 Erreur de connexion: {str(e)}")
    print("Vérifiez que l'API est bien démarrée sur http://localhost:8000")