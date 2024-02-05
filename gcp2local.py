from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator

# Define the DAG with the provided default arguments and schedule interval
dag = DAG(
    'bigquery_to_local',
    description='A DAG to export BigQuery data to local system',  # Set the desired schedule interval, or None if you want to trigger it manually
    catchup=False,  # Set to False if you don't want historical dag runs to run
    tags=['bigquery', 'local'],
    start_date=datetime(2023, 1, 1),
)

# Export data from BigQuery to Google Cloud Storage
export_to_gcs = BigQueryToGCSOperator(
    task_id='export_to_gcs',
    source_project_dataset_table='`playground-s-11-d97226c7`.airflowdataset.data',  # Specify your BigQuery table
    destination_cloud_storage_uris=['gs://airflowdata/data.json'],  # Specify your GCS destination path
    export_format='JSON',
    project_id ='playground-s-11-d97226c7',
    dag=dag,
)

# Download data from GCS to local system
download_to_local = GCSToLocalFilesystemOperator(
    task_id='download_to_local',
    bucket='gs://airflow7487',  # Specify your GCS bucket name
    object_name='spotifydata.json',  # Specify the file name in GCS
    filename='D:\SPOTIFY\Data\spotifydata.json',  # Specify the local file path where you want to save the data  # Specify the GCS connection ID configured in Airflow
    dag=dag,
)

# Set task dependencies
export_to_gcs >> download_to_local
