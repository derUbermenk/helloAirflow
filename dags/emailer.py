#!/usr/bin/env python

import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount 

emailer = DAG(
    dag_id="emailer",
    description = "pseudo sends emails. just saves to csv",
    start_date=datetime.datetime(2024,4,19),
    end_date=datetime.datetime(2024,6,1),
    schedule_interval="@daily"
)

format_emails = DockerOperator(
    task_id = "format_emails",
    image = "format_emails",
    dag=emailer,
    command = [
        "format_emails",
        "./users/users.csv"
        "{{ds}}",
        "./emails/{{ds}}_emails.json"
    ],
    mounts = [
        Mount(source="../volumes/emails", target="/emails", type="bind"),
        Mount(source="../volumes/users", target="/users", type="bind"),
    ]
)

send_emails = DockerOperator(
    task_id = "send_emails",
    image = "send_emails",
    dag=emailer,
    command = [
        "send_emails",
        "{{ds}}",
        "./emails/{{ds}}_emails.json",
        "./logs/{{ds}}_logs.log"
    ],
    mounts = [
        Mount(source="../volumes/emails", target="/emails", type="bind"),
        Mount(source="../volumes/logs", target="/logs", type="bind"),
    ]
)

format_emails >> send_emails