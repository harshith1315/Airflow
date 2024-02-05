from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import storage
import pyodbc
import json

# Define your Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'gcs_to_mssql',
    default_args=default_args,
    schedule_interval=None,  # Set your desired schedule interval here, or None for manual execution
    catchup=False,
    tags=['gcs', 'mssql'],
)

def read_data_from_gcs():
    gcs_bucket_name = 'airflowdata'
    gcs_blob_name = 'data1.json'
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_blob_name)
    json_data = json.loads(blob.download_as_text())
    return json_data

def migrate_data_to_mssql(**kwargs):
    
    mssql_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-SB056D8;DATABASE=sqlnew;UID=harshith;PWD=harshith'

    json_data = read_data_from_gcs()

    # Write data to MSSQL database
    conn = pyodbc.connect(mssql_connection_string)
    cursor = conn.cursor()
        # Assuming 'json_data' is a list of dictionaries in JSON format
    for record in json_data:
            # Customize this SQL query based on your table schema
        query = "INSERT INTO data (USER_OVERALL_RATING, PREDICTED_OVERALL_RATING,CLEANLINESS,LOCATION,VALUE,ROOMS,SERVICE,SLEEP_QUALITY) VALUES (?, ?,?,?,?,?,?,?)"
        cursor.execute(query, record['USER_OVERALL_RATING'], record['PREDICTED_OVERALL_RATING'],record['CLEANLINESS'],record['LOCATION'],record['VALUE'],record['ROOMS'],record['SERVICE'],record['SLEEP_QUALITY'])
    conn.commit()
    cursor.close()
    conn.close()

# Define the PythonOperator task to run the migration function
migration_task = PythonOperator(
    task_id='migrate_gcs_to_mssql',
    python_callable=migrate_data_to_mssql,
    provide_context=True,
    dag=dag,
)

# Set task dependencies if needed
# migration_task.set_upstream(...)
# migration_task.set_downstream(...)

if __name__ == "__main__":
    dag.cli()
