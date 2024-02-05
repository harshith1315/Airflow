from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

# Define the DAG with the provided default arguments and schedule interval
dag = DAG(
    'bigquery_to_gcs',
    #description='A DAG to export BigQuery data to GCS',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Set the desired schedule interval, or None if you want to trigger it manually
    catchup=False,  # Set to False if you don't want historical dag runs to run
    tags=['bigquery', 'gcs'],
)

# Export data from BigQuery to Google Cloud Storage
export_to_gcs = BigQueryToGCSOperator(
    task_id='export_to_gcs',
    source_project_dataset_table='playground-s-11-0f9762b4.airflowdataset.data',  # Specify your BigQuery table
    destination_cloud_storage_uris=['gs://airflowbucket1234/data.csv'],  # Specify your GCS destination path
    export_format='CSV',  # Export format (can be CSV as well)
    dag=dag,
)



# Set task dependencies if you have more tasks in the DAG
export_to_gcs #>> another_task

# You can define more tasks if needed