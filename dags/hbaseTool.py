from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from airflow.hooks.mysql_hook import MySqlHook

import concurrent
from functools import partial

from datetime import datetime, timedelta
import logging
import pendulum
import os


local_tz = pendulum.timezone('Asia/Taipei')
default_args = {
    'owner': 'HbaseDemo',
    'start_date': datetime(2020, 5, 1, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# Hbase Config
hbase_host = 'localhost'
hnase_port = 9090

table_name = 'booking'

booking_prefix = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

booking_columns = [
    b'booking:page_url',
    b'booking:hotel',
    b'booking:ratings',
    b'booking:description',
    b'booking:facilities',
    b'booking:comments',
    b'booking:photo'
]


def download_hbase_table(table_name, table_columns, start_day, prefix_key):
    logging.info(f"Start Download HBase table= {table_name} \n start day = {start_day} columns = {table_columns}")
    down_func = partial(pull, table_name, table_columns, start_day)

    try:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(down_func, prefix_key)
        logging.info(f'Download booking Done!')
    except Exception as ex:
        logging.info(f"Download booking Failed!!!")


def pull(table_name, columns, start_day, prefix_key):
    connection = happybase.Connection(hbase_host, hbase_port)
    logging.info("connect to HBASE")
    
    table = connection.table(table_name)
    day_time = f'_{start_day}'
    list_day = [prefix + day_time  for prefix in prefix_key]

    # Load data from habse
    
    for index, kdata in enumerate(list_day):
        prefix = kdata
        logging.info(f'Scan prefix = {prefix}')
        scanner = table.scan(row_prefix=prefix.encode(), batch_size=100000, columns=columns)
        dat = []
        for key, data in scanner:
            data[b'prefix:rowkey'] = key
            data_in = dict((k.decode('utf8').split(':')[1], v.decode('utf8')) for k, v in data.items())
            dat.append(data_in)
        logging.info('chunck size = %s', len(dat))


def pullData(**context):
    start_date = context['execution_date'].strftime('%Y%m%d')

    download_hbase_table(table_name, booking_columns, start_day, local_save_path, booking_prefix)


with DAG('HbaseDemo', default_args=default_args,schedule_interval='@daily') as dag:
    pull_data = PythonOperator(
        task_id = 'pullData',
        python_callable = pullData,
        provide_context = True
    )
