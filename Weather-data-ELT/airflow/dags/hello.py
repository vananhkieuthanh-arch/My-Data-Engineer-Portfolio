from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["smoke_test"],
) as dag:
    BashOperator(
        task_id="say_hello",
        bash_command='echo "Hello, Airflow!"', 
    )

