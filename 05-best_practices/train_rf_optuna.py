import pandas as pd
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    classification_report,
)
from sklearn.model_selection import train_test_split

# 🔧 Paramètres optimisés
BEST_PARAMS = {
    "n_estimators": 58,
    "max_depth": 28,
    "min_samples_split": 4,
    "min_samples_leaf": 4,
    "class_weight": None,
    "random_state": 42,
}


def load_data():
    X = pd.read_csv("processed_data/X_prepared.csv")
    y = pd.read_csv("processed_data/y_prepared.csv").squeeze()
    return X, y


def evaluate_and_log(model, X_test, y_test, y_pred, y_proba):
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_proba)

    print("📊 Evaluation :")
    print(f"  - Accuracy : {acc:.4f}")
    print(f"  - F1-score : {f1:.4f}")
    print(f"  - ROC AUC  : {roc:.4f}")
    print("\n🧾 Classification Report :\n",
          classification_report(y_test, y_pred)
          )

    mlflow.log_metrics({"accuracy": acc, "f1_score": f1, "roc_auc": roc})


if __name__ == "__main__":
    print("📦 Chargement des données...")
    X, y = load_data()

    # 🔀 Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 🧠 Modèle
    model = RandomForestClassifier(**BEST_PARAMS)
    model.fit(X_train, y_train)

    # 🔍 Prédictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 🚀 MLflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("chicago-traffic-rf")

    with mlflow.start_run():
        mlflow.log_params(BEST_PARAMS)
        evaluate_and_log(model, X_test, y_test, y_pred, y_proba)
        mlflow.sklearn.log_model(model, artifact_path="model")
        print("✅ Modèle sauvegardé dans MLflow.")
