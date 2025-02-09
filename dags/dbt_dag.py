from workflow_tools.dbt.operators.parser_std import DbtDagParser
from airflow import DAG
from datetime import datetime, timedelta
import os

dbt_project_dir = os.getenv('DBT_JAFFLE_SHOP_PATH', '/opt/airflow/dbt_projects/jaffle_shop')

with DAG(
    dag_id="dbt_jaffle_shop",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@once",
    tags=["dbt", "jaffle_shop"],
    dagrun_timeout=timedelta(hours=24),
    catchup=False,
    default_args={
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(minutes=60),
    },
) as dag:
    dag = DbtDagParser(
        dag=dag,
        dbt_project_dir=dbt_project_dir,
        dbt_profiles_dir=dbt_project_dir,
        dbt_target="dev",
        dbt_run_group_name="dbt_run",
        dbt_test_group_name="dbt_test",
    )
