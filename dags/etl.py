from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import json

# Define the DAG
with DAG(
    dag_id = "nasa_etl",
    start_date = datetime(2025, 6, 18, 6, 0),
    schedule = "@daily",
    catchup = True,
    tags = ['portofolio']
) as dag:

    # Task 1: Create table if it doesn't exist
    @task
    def create_table():
        # initialize the postgreshook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        # sql query to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS nasa_apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            date DATE,
            media_type VARCHAR(50),
            url VARCHAR(255)
        );
        """

        # execute the create_table_query
        postgres_hook.run(create_table_query)

    # Task 2: Extract the NASA API Data [Extract Pipeline]
    # API : ZBUe0SkSsZOOfwb6UErrIbmKasN2nbgw17H1BU53
    extract_apod = SimpleHttpOperator(
        task_id="extract_apod",
        http_conn_id="nasa_api",
        endpoint="planetary/apod?api_key={{ conn.nasa_api.extra_dejson.api_key }}&date={{ macros.ds_add(ds, 0) }}",
        method="GET",
        response_filter=lambda response: response.json(),
        log_response=True,
    )


    # Task 3: Transform the data (filtering the information that i need to save) [Transform Pipeline]
    @task
    def transform_data(response):
        apod_data = {
            "title" : response.get("title", ""),
            "explanation" : response.get("explanation", ""),
            "date" : response.get("date", ""),
            "media_type" : response.get("media_type", ""),
            "url" : response.get("url", "")
        }
        
        return apod_data

    # Task 4: Load data into PostgresSQL [Load Pipeline]
    @task
    def load_to_postgres(apod_data):
        # initialize postgres hook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        # sql query to insert to nasa_apod_data table
        insert_query = """
        INSERT INTO nasa_apod_data (title, explanation, date, media_type, url)
        VALUES (%s, %s, %s, %s, %s);
        """
        # execute the insert_query
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['date'],
            apod_data['media_type'],
            apod_data['url']
        ))

    # Task 5: Verify the data through DBeaver


    # Define the task dependencies
    create_table() >> extract_apod
    transformed_data = transform_data(extract_apod.output)
    load_to_postgres(transformed_data)
