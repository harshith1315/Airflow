from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd
from google.cloud import bigquery

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'bigquery_to_gcs_and_snowflake',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
)

def read_bigquery_data(**kwargs):
    project_id = 'playground-s-11-5a8cdbe9'
    dataset_id = 'airflowdataset'
    table_id = 'airflowdata'

    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct a reference to the dataset and table
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Fetch the data from BigQuery into a Pandas DataFrame
    query = f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}"
    df = client.query(query).to_dataframe()

    # Save the DataFrame to a CSV file in GCS
    gcs_bucket_name = 'us-central1-test-c739a870-bucket'
    gcs_filepath = f'gs://{gcs_bucket_name}/test/bigquery_data.csv'
    df.to_csv(gcs_filepath, index=False)

    # Return the GCS filepath, which will be available in the context
    return {'gcs_filepath': gcs_filepath}

def load_data_to_snowflake(**kwargs):
    # Retrieve the GCS filepath from the context
    gcs_filepath = kwargs['task_instance'].xcom_pull(task_ids='extract_data')['gcs_filepath']

    # Read the CSV file from GCS into a DataFrame
    df = pd.read_csv(gcs_filepath)

    user_login_name = 'harshith'
    password = 'Harshith1234'
    account_identifier = 'WKHXVPS.DW82745'

    engine = create_engine(
        'snowflake://{user}:{password}@{account_identifier}/?warehouse={warehouse}&database={database}&schema={schema}'.format(
            user=user_login_name,
            password=password,
            account_identifier=account_identifier,
            warehouse='COMPUTE_WH',  # Replace with your warehouse name
            database='AIRFOWDATA',
            schema='BQDATA',
        )
    )

    # Write the DataFrame to Snowflake
    df.to_sql(name='TRANSDATA', con=engine, index=False, if_exists='replace')

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=read_bigquery_data,
    provide_context=True,  # Add this line to provide the context to the callable function
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_snowflake',
    python_callable=load_data_to_snowflake,
    provide_context=True,  # Add this line to provide the context to the callable function
    dag=dag,
)

# Define the execution order using set_downstream
extract_task >> load_task
