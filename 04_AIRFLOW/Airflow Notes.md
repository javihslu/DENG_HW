Airflow Notes

1	Run Airflow in a docker following these instructions https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.htmlNow 
2	 we want to access our data in gcs and create an external and a partitioned table. For that, make sure you  have a google cloud bucket with the data for yellow taxi in n there. You can run the python script in here https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse/extras  
3	   Now We need to mount our json key to the docker. Add it to your docker-compose file. 
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    # For backward compatibility, with Airflow <2.3
    AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    GOOGLE_APPLICATION_CREDENTIALS: /opt/airflow/keys/gcp-key.json
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth'
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./keys:/opt/airflow/keys
    - ./plugins:/opt/airflow/plugins

4.	Under Admin >> Variables in Airflow GUI add your variables. 
5.	Add conn id under connections  
