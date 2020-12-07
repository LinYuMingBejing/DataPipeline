from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

from datetime import datetime, timedelta
import json
import pendulum
import requests

from tasks.ptt import upsert
from model.PTT import get_table_name


local_tz = pendulum.timezone('Asia/Taipei')
default_args = {
    'owner': 'PTT',
    'start_date': datetime(2020, 5, 1, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# PTT config
PTTUrl  = 'https://moptt.azurewebsites.net/api/v2/hotpost?b=Gossiping&b=Boy-Girl&b=Beauty&b=marvel&b=WomenTalk&b=movie'
headers = Variable.get('User-Agent')
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'Referer': 'https://moptt.tw/',
        'Authorization': 'cMIS1Icr95gnR2U19hxO2K7r6mYQ96vp'
}

def create_table(**context):
    execution_date = context['execution_date'].strftime('%Y%m%d%H')
    table_name = f'HotArticle_{execution_date}'

    from tasks.ptt import create_table

    create_table(table_name)

    return table_name


def crawlPTT(**context):
    table_name = context['task_instance'].xcom_pull(task_ids='createTable')
    table_name = get_table_name(table_name)

    response = requests.get(PTTUrl, headers=headers)
    posts = json.loads(response.text)['posts']

    for post in posts:
        upsert(post, table_name)


with DAG('HotArticle', default_args=default_args,schedule_interval='@hourly') as dag:
    crawlPTT = PythonOperator(
        task_id = 'crawlPTT',
        python_callable = crawlPTT,
        provide_context = True
    )

    createTable = PythonOperator(
        task_id = 'createTable',
        python_callable = create_table,
        provide_context = True
    )

    createTable >> crawlPTT