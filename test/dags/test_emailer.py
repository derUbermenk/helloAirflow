import pytest 
from dags.emailer import emailer
from airflow.utils.dag_cycle_tester import check_cycle 
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.exceptions import AirflowDagCycleException

dag = emailer

def test_dag_should_exist():
    expected_id = dag.dag_id 
    
    assert emailer.dag_id == expected_id, "dag should exist"

def test_dag_tasks():
    tasks = dag.tasks


    task_ids = [task.task_id for task in tasks]

    expected_task_ids = [
        "format_emails",
        "pseudo_send_emails"
    ]

    assert task_ids == expected_task_ids, "dag should have all expected tasks"

def test_dag_should_have_no_cycle():
    did_not_raise_cycle_error = True 

    try:
        check_cycle(dag)
    except AirflowDagCycleException:
        did_not_raise_cycle_error = False 

    assert did_not_raise_cycle_error, "dag should not have a cycle"