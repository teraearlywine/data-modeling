from datetime import timedelta
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import sys

sys.path.append('/scripts')

dag = DAG(
     'recipe_elt_dag'
    , description = 'ELT dag for recipe api, extract & load scripts'
    , schedule_interval = timedelta(days = 1)
    , start_date = days_ago(1)
)

run_api_task = BashOperator(
      task_id = 'run_api_function'
    , bash_command = 'python3 recipe_database.py'
    , dag=dag
)

extract_recipes_task = BashOperator(
      task_id = 'extract_recipes_data'
    , bash_command = 'python3 extract_recipes_full.py'
    , dag = dag
)

load_recipes_bq_task = BashOperator(
      task_id =  'load_recipes_bq'
    , bash_command = 'python3 load_recipes_bq.py'
    , dag = dag
)

run_api_task >> extract_recipes_task
extract_recipes_task >> load_recipes_bq_task