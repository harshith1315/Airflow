from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
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
    schedule_interval='@daily',  # Adjust the schedule based on your requirements
    catchup=False,
)

def read_bigquery_data(**kwargs):
    project_id = 'playground-s-11-28a5a2aa'
    dataset_id = 'airflowdataset'
    table_id = 'airflowtable'

    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct a reference to the dataset and table
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Fetch the data from BigQuery into a Pandas DataFrame
    query = f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}"
    df = client.query(query).to_dataframe()

    return df

def load_data_to_snowflake(**kwargs):
    snowflake_conn_id = 'snowflake_conn'
    dwh_hook = SnowflakeHook(snowflake_conn_id=snowflake_conn_id)

    # Assuming you have the snowflake_table defined somewhere
    snowflake_table = 'MIGRATEDDATA'

    # Get the DataFrame from the XCom
    df = kwargs['ti'].xcom_pull(task_ids='extract_data')

    # Convert DataFrame to list of tuples
    rows = df.to_records(index=False).tolist()

    # SQL query to insert data
    insert_query = f"""
        INSERT INTO {snowflake_table} (USER_OVERALL_RATING, PREDICTED_OVERALL_RATING, CLEANLINESS, LOCATION, VALUE, ROOMS, SERVICE, SLEEP_QUALITY)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Execute the insert query for each row in the data
    for row in rows:
        # Execute the insert query
        dwh_hook.run(insert_query, parameters=row)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=read_bigquery_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_snowflake',
    python_callable=load_data_to_snowflake,
    provide_context=True,
    dag=dag,
)

# Define the execution order
extract_task >> load_task
