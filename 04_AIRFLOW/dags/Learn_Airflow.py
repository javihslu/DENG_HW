# considering the following DAG and the errors, fix the issues and run the DAG successfully.
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd 

Data_path = "/opt/airflow/data"
FILE_PATH = f"{Data_path}/green_tripdata_2019-01.parquet"
def read_parquet():
    df = pd.read_parquet(FILE_PATH)
    print(df.dtypes)    

def create_summary_table():
    df = pd.read_parquet(FILE_PATH)
    summary_table = df.describe()
    print(summary_table) 
    output_path = f"{Data_path}/summary_table.csv"
    summary_table.to_csv(output_path, index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
}   
with DAG(
    'learn_airflow',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    read_parquet_task = PythonOperator(
        task_id='read_parquet',
        python_callable=read_parquet
    )
    create_summary_table_task = PythonOperator(
        task_id='create_summary_table',
        python_callable=create_summary_table
    )   




    read_parquet_task >> create_summary_table_task     

