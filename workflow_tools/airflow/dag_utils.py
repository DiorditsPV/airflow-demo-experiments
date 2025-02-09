from airflow.models import DagRun

# def get_execution_date(dag_id):
#     dag_runs = DagRun.find(dag_id=dag_id)
#     dag_runs.sort(key=lambda x: x.execution_date, reverse=True)
#     dag_last_run = dag_runs[0].execution_date
#     return dag_last_run
#

def get_execution_date(dag_id):
    dag_runs = DagRun.find(dag_id=dag_id)
    
    if not dag_runs:
        raise ValueError(f"DAG - {dag_id} не найден")
    
    latest_run = max(dag_runs, key=lambda run: run.execution_date)
    return latest_run.execution_date 