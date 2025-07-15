# 🚦 Prédiction de la gravité des accidents de la route à Chicago

Ce projet MLOps a pour objectif de prédire si un accident de la circulation à Chicago sera :

- **Sans gravité** : aucun blessé, aucun remorquage
- **Grave** : au moins un blessé **ou** un véhicule remorqué

Les données proviennent du portail open data de la ville de Chicago :
🔗 https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if

## 🎯 Variable cible
Nous utilisons la variable `CRASH_TYPE` pour construire une variable binaire :
- `NO INJURY / DRIVE AWAY` → 0
- `INJURY AND / OR TOW DUE TO CRASH` → 1

## ⚙️ Stack technique prévue
- Python
- MLflow
- Prefect (ou Airflow)
- Docker
- GitHub Actions
- Pandas, Scikit-learn, etc.

## 🚧 État du projet
Projet en cours — première exploration en cours et pipeline en construction.
## ✅ Étapes du projet

- [x] Définir le problème et le jeu de données
- [ ] Explorer et nettoyer les données
- [ ] Créer une cible binaire à partir de `CRASH_TYPE`
- [ ] Entraîner un modèle de base
- [ ] Suivre les expériences avec MLflow
- [ ] Construire un pipeline de formation
- [ ] Déployer le modèle (batch/API)
- [ ] Mettre en place une surveillance du modèle
- [ ] Ajouter un pipeline CI/CD (GitHub Actions)
- [ ] Finaliser la documentation

