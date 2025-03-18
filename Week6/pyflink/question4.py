import pandas as pd
from kafka import KafkaProducer
import json
from time import time

# Read and filter dataset
df = pd.read_csv("green_tripdata_2019-10.csv", usecols=[
    'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'PULocationID', 'DOLocationID', 
    'passenger_count', 'trip_distance', 'tip_amount'
])

# Convert datetime columns to string
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

topic_name = "green-trips"

t0 = time()  # Start timing

# Send data row by row
for _, row in df.iterrows():
    message = row.to_dict()
    producer.send(topic_name, value=message)

# Ensure all messages are sent
producer.flush()

t1 = time()  # End timing
print(f"Time taken to send all messages: {t1 - t0:.2f} seconds")
