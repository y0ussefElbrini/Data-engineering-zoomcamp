import urllib.request
from google.cloud import storage

# Configuration
GCP_BUCKET_NAME = "terraform-demo-week-3"


# List of Parquet URLs
URLS = [
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet"
]


# Initialiser le client GCS
storage_client = storage.Client()
bucket = storage_client.bucket(GCP_BUCKET_NAME)

for url in URLS:
    blob_name = url.split("/")[-1] 
    blob = bucket.blob(blob_name)

    print(f"📥 Téléchargement de {blob_name} depuis {url}...")


    with urllib.request.urlopen(url) as response:
        file_bytes = response.read()  

    print(f"🚀 Upload de {blob_name} vers GCS...")

    # Envoyer directement en tant que fichier binaire
    blob.upload_from_string(file_bytes, content_type="application/octet-stream")

    print(f"✅ {blob_name} a été uploadé avec succès dans {GCP_BUCKET_NAME} !")