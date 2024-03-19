from airflow.models import DagBag, DAG
from dags.emailer import emailer

dag = emailer

def test_dag_should_exist():
    expected_id = dag.dag_id 
    
    assertion = 'dag should exist'
    assert emailer.dag_id == expected_id, assertion

def dag_should_have_no_cycle():
    return