# **NASA APOD ETL Pipeline with Airflow and Postgres**

## **Project Overview**
Proyek ini membangun sebuah ETL Pipeline sederhana menggunakan Apache Airflow untuk mengambil data harian Astronomy Picture of the Day (APOD) dari NASA API, kemudian melakukan transformasi sederhana untuk mengambil informasi yang relevan, dan akhirnya menyimpan data tersebut ke dalam PostgreSQL database. Pipeline ini dapat membantu dalam mengarsipkan dan menganalisis data APOD secara historis.

## **Tools & Technologies**
- Apache Airflow (ETL Orchestration)
- PostgreSQL (Data Storage)
- Docker (Containerization)
- NASA APOD API (Data Source)
- Python (Processing)

## **Pipeline Stages:**
1. Extract: Mengambil data APOD dari NASA API berdasarkan tanggal eksekusi DAG.
2. Transform: Memfilter dan mengambil kolom yang relevan seperti: title, explanation, date, media_type, dan url.
3. Load: Menyimpan hasil transformasi ke tabel nasa_apod_data di PostgreSQL.

## **Schedule**
The pipeline is scheduled to run daily dan akan melakukan catchup untuk mengambil data yang terlewat.

## Additional Note
- Two connection were made in Airflow (my_postgres_connection & nasa_api)