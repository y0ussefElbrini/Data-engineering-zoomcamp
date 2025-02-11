# 📌 Module 3 Homework - Solutions


I started by creating a venv environment

``` bash
python -m venv my_venv
source my_venv/bin/activate
```

and then I installed the necessary libraries :

``` bash
pip install urllib google-cloud-storage
```

then I executed the script `urls_to_gcs.py` :

``` python
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

```

then i created the external table from the parquet files gcs in bigquery using this query (i created a dataset 'yellow_trip_2024' before)

``` SQL
CREATE OR REPLACE EXTERNAL TABLE `terraform-demo-448.yellow_trip_2024.external_yellow_tripdata`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://demo-week-3/yellow_tripdata_2024-*.parquet']
);
```
then i created a materialized table from the external table

``` SQL
create or replace table `terraform-demo-448.yellow_trip_2024.yellow_tripdata`
AS
SELECT * FROM `terraform-demo-448.yellow_trip_2024.external_yellow_tripdata`
```

### question 1

![number of rows in bigquery](images/image1)

### question 2

``` SQL
SELECT count(DISTINCT PULocationID) FROM `terraform-demo-448.yellow_trip_2024.external_yellow_tripdata`
SELECT count(DISTINCT PULocationID) FROM `terraform-demo-448.yellow_trip_2024.yellow_tripdata`
```

### question 3

``` SQL
SELECT PULocationID FROM `terraform-demo-448.yellow_trip_2024.yellow_tripdata`
SELECT PULocationID, DOLocationID FROM `terraform-demo-448.yellow_trip_2024.yellow_tripdata`
```

### question 4

``` SQL
SELECT count(fare_amount) FROM `terraform-demo-448.yellow_trip_2024.yellow_tripdata` where fare_amount = 0
```


### question 5

``` SQL
CREATE OR REPLACE TABLE `terraform-demo-448.yellow_trip_2024.partitioned_clustered_yellow_tripdata`
PARTITION BY TIMESTAMP_TRUNC(tpep_dropoff_datetime, DAY)
CLUSTER BY VendorID
AS
(SELECT * FROM `terraform-demo-448.yellow_trip_2024.yellow_tripdata`)

--verification
select column_name, data_type 
from `terraform-demo-448.yellow_trip_2024.INFORMATION_SCHEMA.COLUMNS`
where table_name = 'partitioned_clustered_yellow_tripdata'

select *
from `terraform-demo-448.yellow_trip_2024.INFORMATION_SCHEMA.PARTITIONS`
```


### question 6

``` SQL
select distinct VendorID from `terraform-demo-448.yellow_trip_2024.yellow_tripdata` where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'
select distinct VendorID from `terraform-demo-448.yellow_trip_2024.partitioned_clustered_yellow_tripdata` where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'
```
