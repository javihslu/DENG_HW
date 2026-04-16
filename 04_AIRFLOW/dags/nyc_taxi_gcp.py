import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.models import Variable


PROJECT_ID = Variable.get("GCP_PROJECT_ID")
BUCKET = Variable.get("GCP_BUCKET_NAME")
BIGQUERY_DATASET = Variable.get("GCP_DATASET", 'dengtaxi')
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/Users/jvr/airflow/airflow/")
# BIGQUERY_DATASET = os.environ.get("GCP_DATASET", 'dengtaxi')

DATASET = "tripdata"
# COLOUR_RANGE = {'green': 'tpep_pickup_datetime'}
COLOUR_RANGE = {'green': 'lpep_pickup_datetime'}
INPUT_PART = "raw"
INPUT_FILETYPE = "parquet"


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="gcs_2_bq_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    for colour, ds_col in COLOUR_RANGE.items():


        bigquery_external_table_task = BigQueryCreateExternalTableOperator(
            task_id=f"bq_{colour}_{DATASET}_external_table_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"{colour}_{DATASET}_external_table",
                },
                "externalDataConfiguration": {
                    "sourceFormat": "PARQUET",
                    "autodetect": True, 
                    "sourceUris": [f"gs://{BUCKET}/{colour}/*"],
                },
            },
        )

        CREATE_BQ_TBL_QUERY = f"""
        CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{colour}_{DATASET}
        PARTITION BY DATE(pickup_ts) AS
        SELECT
            * EXCEPT(`{ds_col}`),
            TIMESTAMP_MICROS(CAST(`{ds_col}` / 1000 AS INT64)) AS pickup_ts
            FROM {BIGQUERY_DATASET}.{colour}_{DATASET}_external_table
        WHERE `{ds_col}` IS NOT NULL;
        """
        # Create a partitioned table from external table
        bq_create_partitioned_table_job = BigQueryInsertJobOperator(
            task_id=f"bq_create_{colour}_{DATASET}_partitioned_table_task",
            configuration={
                "query": {
                    "query": CREATE_BQ_TBL_QUERY,
                    "useLegacySql": False,
                }
            }
        )

        bigquery_external_table_task >> bq_create_partitioned_table_job