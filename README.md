# Data Pipeline + ETL (Simple Version)
### Enviroment:
* Ubuntu: 16.04 
* Python: 3.6.2
* Crawl Framework: Scrapy
* Database: MySQL, Redis
* Pipeline: Airflow


### Deploy Airflow
* Install Redis as Worker

```
$ docker pull redis
$ docker run --name redis-lab -p 6379:6379 -d redis

# Check redis wherether running
$ ps -ef | grep redis
$ losf -i:6369
```

* Install MySQL as Airflow Database

```
$ docker pull mysql:latest
$ docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql
```

mysql -u root -p

```
mysql> create database airflow;
mysql> CREATE USER 'airflow' IDENTIFIED BY 'airflow';
mysql> GRANT ALL PRIVILEGES ON airflow.* to 'airflow'@'%' WITH GRANT OPTION;
mysql> flush privileges;
```

* Enviroment Variables
vim airflow.cfg

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
$ airflow initdb
$ airflow upgradedb
$ export AIRFLOW_HOME="$(pwd)"
$ export PYTHONPATH="$(pwd)"

# start airflow
$ source $AIRFLOW_HOME/env/bin/activate && airflow webserver -p 8080
$ source $AIRFLOW_HOME/env/bin/activate && airflow worker
$ source $AIRFLOW_HOME/env/bin/activate && airflow scheduler
```