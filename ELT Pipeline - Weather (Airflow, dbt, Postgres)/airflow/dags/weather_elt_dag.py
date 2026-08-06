from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "weather_elt_dag",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="weather_elt",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["weather", "elt"],
) as dag:

    extract = BashOperator(
        task_id="extract_data",
        bash_command="cd /opt/airflow && python src/weather_raw.py",
    )

    load = BashOperator(
        task_id="load_data",
        bash_command="cd /opt/airflow && python src/load_raw.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/dbt_project && "
            "dbt run --profiles-dir /opt/airflow/dbt_project"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/dbt_project && "
            "dbt test --profiles-dir /opt/airflow/dbt_project"
        ),
    )

    extract >> load >> dbt_run >> dbt_test
