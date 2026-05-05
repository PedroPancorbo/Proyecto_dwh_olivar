"""
DAG principal del pipeline de la Cooperativa Olivarera.
Orquesta: generación de datos → ingesta RAW → dbt run → dbt test
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PYTHON = "/opt/pipeline-env/bin/python"
DBT    = "/opt/pipeline-env/bin/dbt"

default_args = {
    "owner": "olive",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="olive_pipeline",
    description="Pipeline completo: generación, ingesta RAW y transformaciones dbt",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["olive", "dwh"],
) as dag:

    generar_datos = BashOperator(
        task_id="generar_datos",
        bash_command=f"cd /opt/airflow && {PYTHON} src/generator/generate_data.py",
    )

    ingestar_raw = BashOperator(
        task_id="ingestar_raw",
        bash_command=f"cd /opt/airflow && {PYTHON} src/ingestion/load_raw.py",
        env={
            "POSTGRES_USER": "olive",
            "POSTGRES_PASSWORD": "olive_pwd",
            "POSTGRES_DB": "olive_dwh",
            "POSTGRES_HOST": "postgres",
            "POSTGRES_PORT": "5432",
        },
        append_env=True,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT} run --project-dir /opt/airflow/olive_dwh --profiles-dir /opt/airflow/dbt_profiles",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{DBT} test --project-dir /opt/airflow/olive_dwh --profiles-dir /opt/airflow/dbt_profiles",
    )

    generar_datos >> ingestar_raw >> dbt_run >> dbt_test
