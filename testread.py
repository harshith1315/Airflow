from sqlalchemy import create_engine

# Create a connection to Snowflake using your account and user
snowflake_account = 'https://wkhxvps-dw82745.snowflakecomputing.com'
snowflake_username = 'harshith'
snowflake_password = 'Harshith1234'
snowflake_database='AIRFOWDATA'
snowflake_schema='BQDATA'
snowflake_table='MIGRATEDDATA'

snowflake_conn_str = (
        f"snowflake://{snowflake_username}:{snowflake_password}@{snowflake_account}/"
        f"?database={snowflake_database}&schema={snowflake_schema}"
    )

engine = create_engine(snowflake_conn_str)

# Establish a connection
connection = engine.connect()

sql = f"SELECT * FROM {snowflake_table}"

try:
    # Execute the SQL query
    result = connection.execute(sql)

    # Fetch all the rows from the result
    rows = result.fetchall()

    # Print the column names
    print(result.keys())

    # Print the data
    for row in rows:
        print(row)
finally:
    # Close the connection
    connection.close()
    # Dispose of the engine
    engine.dispose()