from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from airflow.hooks.mysql_hook import MySqlHook

from datetime import datetime, timedelta
import json
import pendulum
import requests

from tasks.ptt import create_table, upsert


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

# MySQL config
mysqlhook = MySqlHook(mysql_conn_id='PTT')

def create_table(**context):
    execution_date = context['execution_date'].strftime('%Y%m%d %H:%M:%S')
    table_name = f'HotArticle_{execution_date}'
    create_table(table_name)
    return table_name


def crawlPTT(**context):
    table_name = context['task_instance'].xcom_pull(task_ids='create_table')
    r = requests.get(PTTUrl,headers=headers)
    posts = json.loads(r.text)

    for post in posts:
        upsert(post)


with DAG('HotArticle', default_args=default_args,schedule_interval='0 9 1 * *') as dag:
    crawlPTT = PythonOperator(
        task_id = 'crawlPTT',
        python_callable = crawlPTT,
        provide_context = True
    )

    createTable = PythonOperator(
        task_id = 'ceateTable',
        python_callable = ceate_table,
        provide_context = True
    )

    createTable >> crawlPTT