#!/usr/bin/env python

import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

emailer = DAG(
    dag_id="emailer",
    description = "pseudo sends emails. just saves to csv",
    start_date=datetime.datetime(2022,1,1),
    end_date=datetime.datetime(2024,2,1),
    schedule="@daily"
)

format_emails = DockerOperator(
    task_id = "format_emails",
    image = "format_emails",
    dag=emailer
) 

send_emails = DockerOperator(
    task_id = "send_emails",
    image = "send_emails",
    dag=emailer
)

format_emails >> send_emails 