from prefect import flow, task
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
from datetime import datetime, timedelta
import pandas as pd
import subprocess
import joblib
import os
import numpy as np
import argparse
from prepare_data import preprocess_data, load_data

def get_default_period():
    """Détecte automatiquement le mois/année précédent"""
    now = datetime.now()
    if now.month == 1:
        return 12, now.year - 1
    return now.month - 1, now.year

@task
def download_new_data_task(month: int, year: int):
    date_str = f"{year:04d}-{month:02d}-01"
    print(f"📥 Téléchargement des données depuis {date_str}...")
    
    url = f"https://data.cityofchicago.org/resource/85ca-t3if.csv?$where=crash_date>'{date_str}'"
    df = pd.read_csv(url)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/new_data.csv", index=False)
    
    print(f"✅ {df.shape[0]} lignes téléchargées.")
    return "data/new_data.csv"

@task
def prepare_and_extend_data_task():
    # Chargement des données
    try:
        df_old = pd.read_csv('data/Traffic_Crashes.csv')
        df_old.columns = df_old.columns.str.lower()
    except FileNotFoundError:
        df_old = pd.DataFrame()

    df_new = load_data("data/new_data.csv")
    df_full = pd.concat([df_old, df_new], ignore_index=True)

    # Prétraitement
    X, y, preprocessor = preprocess_data(df_full)
    
    # Sauvegarde
    os.makedirs("processed_data", exist_ok=True)
    pd.DataFrame(X).to_csv("processed_data/X_prepared.csv", index=False)
    pd.DataFrame(y).to_csv("processed_data/y_prepared.csv", index=False)
    joblib.dump(preprocessor, "processed_data/preprocessor.joblib")
    
    print(f"✅ Données mises à jour : {X.shape[0]} échantillons")
    return X.shape[0]

@task
def train_model_task():
    subprocess.run(["python", "train_rf_optuna.py"], check=True)
    return "✅ Modèle entraîné et logué."

@flow(name="Chicago Traffic - ML Pipeline", persist_result=False)
def main_pipeline(month: int = None, year: int = None):
    # Détection automatique si non spécifié
    month, year = (month, year) if (month and year) else get_default_period()
    
    download_new_data_task(month, year)
    prepare_and_extend_data_task()
    train_model_task()

def deploy():
    """Crée un déploiement programmé"""
    Deployment.build_from_flow(
        flow=main_pipeline,
        name="Training Automatique",
        schedule=IntervalSchedule(interval=timedelta(days=30)),
        work_pool_name="my-pool"
    ).apply()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", type=int, default=None)
    parser.add_argument("--year", type=int, default=None)
    parser.add_argument("--deploy", action="store_true", help="Créer un déploiement programmé")

    args = parser.parse_args()

    if args.deploy:
        deploy()
        print("✅ Déploiement créé. Le pipeline s'exécutera automatiquement chaque mois.")
    else:
        main_pipeline(month=args.month, year=args.year)