import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

emailer = DAG(
    dag_id="emailer",
    start_date=datetime.datetime(2021,1,1),
    schedule="@daily"
)

format_emails = DockerOperator(
    task_id = "format_emails",
    image = "format_emails:latest",
    dag=emailer
) 

pseudo_send_emails = DockerOperator(
    task_id = "pseudo_send_emails",
    image = "pseudo_send_emails:latest",
    dag=emailer
)

format_emails >> pseudo_send_emails 