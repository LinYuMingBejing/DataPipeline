from airflow import DAG
from airflow.operators import BashOperator

from datetime import datetime, timedelta
import pendulum
import os


local_tz = pendulum.timezone('Asia/Taipei')
default_args = {
    'owner': 'www.books.com.tw',
    'start_date': datetime(2020, 12, 1, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


with DAG('Books', default_args=default_args, schedule_interval='@daily') as dag:
    
    t2 = BashOperator(
        task_id = 'crawl',
        bash_command = f'cd {os.environ.get("AIRFLOW_HOME")}/Books && scrapy crawl books',
    )
