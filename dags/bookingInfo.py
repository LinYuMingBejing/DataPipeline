from airflow import DAG
from airflow.operators import BashOperator

from datetime import datetime, timedelta
import pendulum
import os


local_tz = pendulum.timezone('Asia/Taipei')
default_args = {
    'owner': 'Booking',
    'start_date': datetime(2020, 5, 1, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


with DAG('Booking.com', default_args=default_args,schedule_interval='@daily') as dag:
    
    t2 = BashOperator(
        task_id = 'scrapy_hotel_info',
        bash_command = f'cd {os.environ.get("AIRFLOW_HOME")}/hotel && scrapy crawl booking',
    )
            