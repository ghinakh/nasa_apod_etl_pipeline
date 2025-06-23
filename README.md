# **NASA APOD ETL Pipeline with Airflow and Postgres**

## **Project Overview**
This project builds a simple ETL pipeline using Apache Airflow to retrieve the daily Astronomy Picture of the Day (APOD) from the NASA API, perform basic transformation to extract the relevant information, and finally store the data into a PostgreSQL database. This pipeline can help archive and analyze APOD data historically.

## **Tools & Technologies**
- Apache Airflow (ETL Orchestration)
- PostgreSQL (Data Storage)
- Docker (Containerization)
- NASA APOD API (Data Source)
- Python (Processing)

## **Pipeline Stages:**
1. Extract: Retrieve APOD data from the NASA API based on the DAG execution date.
2. Transform: Filter and extract relevant fields such as title, explanation, date, media_type, dan url.
3. Load: Insert the transformed data into the nasa_apod_data table in PostgreSQL.

## **Schedule**
The pipeline is scheduled to run daily and is configured to catch up on any missed runs.

## **Additional Notes**
- Two Airflow connections need to be configured:
    - my_postgres_connection
    - nasa_api