from airflow.models import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime

from utils.preprocess_data import preprocess_data
from utils.experiment import experiment
from utils.save_model_db import save_model_db
from utils.fit_best_model import fit_best_model
# from utils.save_batch_data import save_batch_data
from utils.load_iris_data import load_iris_data

default_args= {
    'owner': 'Samira Alipour',
    'email_on_failure': True,
    'email': ['salipour86.1400@gmail.com'],
    'start_date': datetime(2021, 12, 1)
}

with DAG("ml_pipeline",
    description="ML pipeline",
    schedule_interval='@daily',
    default_args=default_args, 
    catchup=False) as dag:



    # task: 0
    load_iris_ = PythonOperator(
        task_id='load_iris_data',
        python_callable=load_iris_data,
    )
    
    # task: 1
    preprocess_data_ = PythonOperator(
        task_id = 'preprocess_data',
        python_callable = preprocess_data
        )

    # task: 2
    grid_search_ = PythonOperator(
        task_id='grid_search',
        python_callable=experiment,
    )
    
    #task 3
    create_gridsearch_table_ = PostgresOperator(
        task_id = 'create_gridsearch_table',
        postgres_conn_id ='postgres_default1',
        sql='sql/create_experiments.sql',
        )

    # task: 4       
    saving_results_ = PythonOperator(
        task_id='saving_results',
        python_callable=save_model_db,
    )

   

    load_iris_ >> preprocess_data_ >> grid_search_ >> create_gridsearch_table_ >> saving_results_