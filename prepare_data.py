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
        self.freq_maps = {}

    def fit(self, X, y=None):
        for col in X.columns:
            freq = X[col].value_counts(normalize=True)
            self.freq_maps[col] = freq
        return self

    def transform(self, X):
        X_encoded = X.copy()
        for col in X.columns:
            X_encoded[col] = X[col].map(self.freq_maps[col]).fillna(0)
        return X_encoded

# 3. Prétraitement
def preprocess_data(df):
    selected_cols = [
    'POSTED_SPEED_LIMIT', 'WEATHER_CONDITION', 'LIGHTING_CONDITION',
    'FIRST_CRASH_TYPE', 'TRAFFICWAY_TYPE', 'ROADWAY_SURFACE_COND',
    'PRIM_CONTRIBUTORY_CAUSE', 'CRASH_HOUR', 'CRASH_TYPE','delay_police_minutes'
    ]
    
    # Conversion des colonnes de dates
    df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], errors='coerce')
    df['DATE_POLICE_NOTIFIED']= pd.to_datetime(df['DATE_POLICE_NOTIFIED'], errors='coerce')
    # Calcul du délai entre la date de l'_accident et la date à laquelle la police a été notifiée
    df['delay_police_minutes'] = (df['DATE_POLICE_NOTIFIED'] - df['CRASH_DATE']).dt.total_seconds() / 60

    df = df[selected_cols].copy()

    # Cible
    df["target"] = df["CRASH_TYPE"].apply(lambda x: 1 if x == 'INJURY AND / OR TOW DUE TO CRASH' else 0)
    df.drop(columns=["CRASH_TYPE"], inplace=True)

    # Colonnes
    categorical_onehot = ['WEATHER_CONDITION', 'LIGHTING_CONDITION']
    categorical_freq = ['FIRST_CRASH_TYPE', 'TRAFFICWAY_TYPE', 'ROADWAY_SURFACE_COND', 'PRIM_CONTRIBUTORY_CAUSE']
    numeric_cols = ['POSTED_SPEED_LIMIT', 'CRASH_HOUR','delay_police_minutes']

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
def save_data(X, y, preprocessor, output_dir='processed'):
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(X, f"{output_dir}/X.joblib")
    joblib.dump(y, f"{output_dir}/y.joblib")
    joblib.dump(preprocessor, f"{output_dir}/preprocessor.joblib")
    print("💾 Données et préprocesseur sauvegardés.")

# 5. Main
if __name__ == "__main__":
    df = load_data("data/Traffic_Crashes_-_Crashes.csv")
    X, y, preprocessor = preprocess_data(df)
    save_data(X, y, preprocessor)
