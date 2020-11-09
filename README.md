# Data Pipeline + ETL (Simple Version)
### Enviroment:
* Ubuntu: 16.04 
* Python: 3.6.2
* Crawl Framework: Scrapy
* Database: MySQL, Redis, Hbase
* Pipeline: Airflow



## Deploy Airflow
* Install Redis as Worker
> You can work airflow which is scaled out with celery and redis.

```
$ docker pull redis
$ docker run --name redis-lab -p 6379:6379 -d redis

 # Check redis wherether running
$ ps -ef | grep redis
$ losf -i:6369
```

* Install MySQL
>  Airflow will store any configurations such as DAG name, default args, connection settings and variables in MySQL. 

```
$ docker pull mysql:latest
$ docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql
```

```
mysql -u root -p

mysql> create database airflow;
mysql> CREATE USER 'airflow' IDENTIFIED BY 'airflow';
mysql> GRANT ALL PRIVILEGES ON airflow.* to 'airflow'@'%' WITH GRANT OPTION;
mysql> flush privileges;
```


* Init DB
> The following command will automatically create dags/, logs/, airflow.db and unittests.cfg.
Airflow will automatically read files in dags folder.

```
$ airflow initdb
```

* Enviroment Variables
```
$ vim airflow.cfg
```

```
AIRFLOW_CONFIG=/root/Article/airflow.cfg
AIRFLOW_HOME=/root/Article
PYTHONPATH=/root/Article

C_FORCE_ROOT=true

AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Taipei
AIRFLOW__CORE__LOAD_EXAMPLES=False

AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CELERY_BROKER_URL=redis://localhost:6379/1
AIRFLOW__CELERY_RESULT_BACKEND=redis://localhost:6379/2

AIRFLOW__CORE__SQL_ALCHEMY_CONN=mysql://airflow:airflow@localhost:3306/airflow

SQLALCHEMY_POOL_RECYCLE=500

```


* Deploy

```
$ airflow upgradedb
$ export AIRFLOW_HOME="$(pwd)"
$ export PYTHONPATH="$(pwd)"

# start airflow
$ source $AIRFLOW_HOME/env/bin/activate && airflow webserver -p 8080
$ source $AIRFLOW_HOME/env/bin/activate && airflow worker
$ source $AIRFLOW_HOME/env/bin/activate && airflow scheduler
```

> ##### Reference
> * https://github.com/DansProjects/airflow-averageface
> * https://leemeng.tw/a-story-about-airflow-and-data-engineering-using-how-to-use-python-to-catch-up-with-latest-comics-as-an-example.html