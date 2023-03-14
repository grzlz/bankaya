import pandas as pd
import boto3
import os
from pymongo import MongoClient
from datetime import datetime
import psycopg2

# MongoDB

# Connect to the local db
client = MongoClient('localhost', 27017)

# Select database
db = client['test']

# Define the names of the collections to fetch
collection_names = ['items_data', 'customers_data', 'bought_items']

# Connect to S3 bucket
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket_name = 'bakaya-dl-challenge'

# Fetch the data from MongoDB and put it in S3
for collection_name in collection_names:
    collection_data = db[collection_name].find({})
    df = pd.DataFrame(collection_data)
    df = df.astype(str)
    key = f"mongo_data_{collection_name}_{datetime.now().strftime('%Y-%m-%d')}.parquet"
    s3.put_object(Body=df.to_parquet(), Bucket=bucket_name, Key=key)
    print(f"Succesfully loaded file {collection_name}")

# Postgres
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    database='bankaya',
    user='postgres',
    password=POSTGRES_PASSWORD
)


# Connect to S3 bucket
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket_name = 'bakaya-dl-challenge'

table_names = ['customer_tbl', 'item_tbl', 'item_purchase_tbl']

for table_name in table_names:
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    key = f"postgres/{table_name}_{datetime.now().strftime('%Y-%m-%d')}.parquet"
    s3.put_object(Body=df.to_parquet(), Bucket=bucket_name, Key=key)
# Print the table names
print(table_names) 