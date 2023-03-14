import pandas as pd
import boto3
import os
from pymongo import MongoClient
from datetime import datetime
import psycopg2
from create_table_statements import create_table_statements
from sqlalchemy import create_engine
from io import BytesIO


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

# Put data in S3 bucket
for table_name in table_names:
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    key = f"postgres/{table_name}_{datetime.now().strftime('%Y-%m-%d')}.parquet"
    s3.put_object(Body=df.to_parquet(), Bucket=bucket_name, Key=key)
    print(f"Succesfully loaded file {table_name}")

# Then extract from S3 and load into data warehouse
folder_path = 'postgres/'
s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket = s3_resource.Bucket(bucket_name)
parquet_files = [obj.key for obj in bucket.objects.filter(Prefix=folder_path) if obj.key.endswith('.parquet')]

# Rearrange list to prevent foreign key issues
parquet_files = [parquet_files[0], parquet_files[2], parquet_files[1]]

conn = psycopg2.connect(
    host='localhost',
    database='bankaya_dwh',
    user='postgres',
    password=POSTGRES_PASSWORD
)
cursor = conn.cursor()
for create_table in create_table_statements:
    cursor.execute(create_table)
    conn.commit()

engine = create_engine(f'postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/bankaya_dwh')

# Print the list of files
for parquet_file in parquet_files:
    print(parquet_file)
    # Load the Parquet file as a pandas dataframe
    file = bucket.Object(parquet_file).get()
    df = pd.read_parquet(BytesIO(file['Body'].read()))
    parts = parquet_file.split('/')
    table_name = parts[-1].split('.')[0].split('_')[0:-1]
    table_name = '_'.join(table_name)
    print(df)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print(f"Succesfully loaded data into {table_name}")

engine.dispose()