import datetime

from airflow import DAG

emailer = DAG(
    dag_id="emailer",
    start_date=datetime.datetime(2021,1,1),
    schedule="@daily"
)