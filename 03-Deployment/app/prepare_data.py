# prepare_data.py

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

# 1. Chargement
def load_data(path):
    df = pd.read_csv(path)
    return df

# 2. Encodage par fréquence
class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.freq_maps = []

    def fit(self, X, y=None):
        self.freq_maps = []
        for i in range(X.shape[1]):
            values, counts = np.unique(X[:, i], return_counts=True)
            freqs = counts / counts.sum()
            self.freq_maps.append(dict(zip(values, freqs)))
        return self

    def transform(self, X):
        X_encoded = np.zeros_like(X, dtype=float)
        for i in range(X.shape[1]):
            map_i = self.freq_maps[i]
            X_encoded[:, i] = [map_i.get(val, 0) for val in X[:, i]]
        return X_encoded

# 3. Prétraitement
def preprocess_data(df):
    selected_cols = [
        'posted_speed_limit', 'weather_condition', 'lighting_condition',
        'first_crash_type', 'trafficway_type', 'roadway_surface_cond',
        'prim_contributory_cause', 'crash_hour', 'crash_type', 'delay_police_minutes'
    ]

    # Conversion des colonnes de dates
    df['crash_date'] = pd.to_datetime(df['crash_date'], errors='coerce')
    df['date_police_notified'] = pd.to_datetime(df['date_police_notified'], errors='coerce')

    # Calcul du délai entre la date de l'accident et la date à laquelle la police a été notifiée
    df['delay_police_minutes'] = (df['date_police_notified'] - df['crash_date']).dt.total_seconds() / 60

    df = df[selected_cols].copy()

    # Cible
    df["target"] = df["crash_type"].apply(lambda x: 1 if x == 'INJURY AND / OR TOW DUE TO CRASH' else 0)
    df.drop(columns=["crash_type"], inplace=True)

    # Colonnes
    categorical_onehot = ['weather_condition', 'lighting_condition']
    categorical_freq = ['first_crash_type', 'trafficway_type', 'roadway_surface_cond', 'prim_contributory_cause']
    numeric_cols = ['posted_speed_limit', 'crash_hour', 'delay_police_minutes']


    # Pipelines
    cat_ohe_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    cat_freq_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('freq', FrequencyEncoder())
    ])

    num_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('cat_ohe', cat_ohe_pipeline, categorical_onehot),
        ('cat_freq', cat_freq_pipeline, categorical_freq),
        ('num', num_pipeline, numeric_cols)
    ])

    X = df.drop(columns='target')
    y = df['target']
    X_transformed = preprocessor.fit_transform(X)

    print(f"✅ Données transformées : {X_transformed.shape}")
    return X_transformed, y, preprocessor

# 4. Sauvegarde
def save_data(X, y, preprocessor, output_dir='processed_data'):
    os.makedirs(output_dir, exist_ok=True)
    
    # Sauvegarde en .joblib
    joblib.dump(preprocessor, f"{output_dir}/preprocessor.joblib")
    
    # Sauvegarde en CSV pour visualisation (optionnelle)
    pd.DataFrame(X).to_csv(f"{output_dir}/X_prepared.csv", index=False)
    pd.DataFrame(y).to_csv(f"{output_dir}/y_prepared.csv", index=False)
    
    print("💾 Données et préprocesseur sauvegardés.")

# 5. Main
if __name__ == "__main__":
    df = load_data("Traffic_Crashes.csv")
    X, y, preprocessor = preprocess_data(df)
    save_data(X, y, preprocessor)
