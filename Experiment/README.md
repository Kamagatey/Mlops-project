# Prédiction de la Gravité des Accidents de la Route à Chicago - Projet MLOps

Ce projet MLOps a pour objectif de prédire si un accident de la circulation à Chicago sera :

- **Sans gravité** : aucun blessé **et** aucun remorquage
- **Grave** : au moins un blessé **ou** un véhicule remorqué

L'approche repose sur un modèle de classification supervisée, et l'ensemble du pipeline suit les bonnes pratiques de l'ingénierie MLOps, notamment en matière de :

- Suivi d’expériences avec **MLflow**
- Optimisation d’hyperparamètres avec **Optuna**
- Séparation claire des données d’entraînement et de validation
- Journalisation des métriques, paramètres, et artefacts pour chaque expérience

Ce projet s'inspire de l'approche présentée dans le **MLOps Zoomcamp (DataTalksClub)**, en particulier la partie `02-experiment-tracking`.


---

## Structure du projet

- `processed_data/` : dossiers contenant les données préparées (`X_prepared.csv` et `y_prepared.csv`)  
- `experimentation.ipynb` : script principal pour entraîner les modèles (baseline et optimisation hyperparamètres)  
- `mlflow.db` : base de données SQLite utilisée pour le tracking MLflow  
- `requirements.txt` : liste des dépendances Python  
- `README.md` : ce fichier

---

## Fonctionnalités

- Chargement et préparation des données  
- Entraînement d’un modèle baseline (RandomForest)  
- Optimisation d’hyperparamètres avec Optuna  
- Evaluation avec plusieurs métriques (accuracy, F1-score, ROC-AUC)  
- Tracking complet des runs avec MLflow (params, metrics, artefacts, tags)  
- Visualisation des résultats d’optimisation (courbes Optuna)  
- Sauvegarde et test du modèle enregistré

---

## Instructions d’utilisation

1. **Installer les dépendances** :

```bash
pip install -r requirements.txt
