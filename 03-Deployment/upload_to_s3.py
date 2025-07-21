import boto3
import os
from pathlib import Path

BUCKET_NAME = "mlops-models"
ENDPOINT = "http://localhost:4566"  # LocalStack
MODEL_DIR = "app/model"

# Configuration S3
s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id="test",  # Identifiants factices pour LocalStack
    aws_secret_access_key="test",
    region_name="us-east-1"
)

def check_and_create_bucket():
    """Vérifie et crée le bucket si nécessaire"""
    try:
        buckets = s3.list_buckets()
        if not any(b['Name'] == BUCKET_NAME for b in buckets['Buckets']):
            s3.create_bucket(Bucket=BUCKET_NAME)
            print(f"✅ Bucket {BUCKET_NAME} créé.")
        else:
            print(f"📦 Bucket {BUCKET_NAME} existe déjà")
    except Exception as e:
        print(f"❌ Erreur avec le bucket: {str(e)}")
        raise

def upload_files():
    """Upload les fichiers vers S3"""
    files = ["model.pkl", "preprocessor.joblib"]
    for file in files:
        file_path = Path(MODEL_DIR) / file
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"Fichier {file_path} introuvable")
            
            s3.upload_file(str(file_path), BUCKET_NAME, file)
            print(f"📤 {file} uploadé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'upload de {file}: {str(e)}")
            raise

if __name__ == "__main__":
    print("🚀 Début de l'upload vers LocalStack S3")
    check_and_create_bucket()
    upload_files()
    print("✅ Téléversement terminé")