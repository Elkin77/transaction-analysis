from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from pymongo import MongoClient
import psycopg2

default_args = {
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'load_transactions_failed_in_postgresql',
    default_args=default_args,
    description='Aggregate failed transactions by date from MongoDB and insert into PostgreSQL',
    schedule_interval=timedelta(days=1),
)

def fetch_from_mongo():
    client = MongoClient('mongodb://root:password@mongodb:27017/')
    db = client['test']
    collection = db['testcollection']
    pipeline = [
        {
            '$match': {
                'Inconsistency_description': { '$ne': None }
            }
        },
        {
            '$addFields': {
                'dateCreatedPay': {
                    '$cond': {
                        'if': { '$not': [{ '$eq': [{ '$type': '$dateCreatedPay' }, 'date'] }] },
                        'then': { '$dateFromString': { 'dateString': '$dateCreatedPay' } },
                        'else': '$dateCreatedPay'
                    }
                }
            }
        },
        {
            '$project': {
                'transaction_date': {
                    '$dateToString': { 'format': '%Y-%m-%d', 'date': '$dateCreatedPay' }
                }
            }
        },
        {
            '$group': {
                '_id': '$transaction_date',
                'failed_transactions': { '$sum': 1 }
            }
        },
        {
            '$sort': { '_id': 1 }
        }
    ]
    data = list(collection.aggregate(pipeline))
    client.close()
    print("Data fetched from MongoDB:", data)
    return data

def insert_into_postgres(data):
    conn = psycopg2.connect(
        dbname='airflow',
        user='airflow',
        password='airflow',
        host='project-postgres',
        port='5432'
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS failed_transactions (
            transaction_date DATE PRIMARY KEY,
            failed_transactions INT NOT NULL
        )
    ''')
    for item in data:
        try:
            cursor.execute('''
                INSERT INTO failed_transactions (transaction_date, failed_transactions)
                VALUES (%s, %s)
                ON CONFLICT (transaction_date) DO NOTHING
            ''', (item['_id'], item['failed_transactions']))
        except Exception as e:
            print("Error inserting item:", item, "Error:", e)
    conn.commit()
    cursor.close()
    conn.close()

def transfer_data(**kwargs):
    data = fetch_from_mongo()
    insert_into_postgres(data)

with dag:
    transfer_task = PythonOperator(
        task_id='transfer_data',
        python_callable=transfer_data,
        provide_context=True,
    )