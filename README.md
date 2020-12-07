# Airflow + ETL (Simple Version)
### Enviroment:
* Ubuntu: 16.04 
* Python: 3.6.2
* Crawl Framework: Scrapy
* Database: MySQL, Redis, Hbase
* Pipeline: Airflow



## Deploy Airflow
### Install Redis as Worker
> You can work airflow which is scaled out with celery and redis.
> You need to be running an right version of Celery.
```
$ docker pull redis
$ docker run --name redis-lab -p 6379:6379 -d redis
```

* Check if Redis server is running
```
$ ps -ef | grep redis
$ lsof -i:6369
```

* Remove a Binding to an IP Address
```
$ vim /etc/redis/redis.conf
```
```
$ #bind 127.0.0.1
```

### Install MySQL
>  Airflow will store any configurations such as DAG name, default args, connection settings and variables in MySQL. 

* Install MySQL
```
$ docker pull mysql:latest
$ docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql
```



* Create a new MySQL user account for Airflow
```
mysql -u root -p root

mysql> create database airflow;
mysql> CREATE USER 'airflow' IDENTIFIED BY 'airflow';
mysql> GRANT ALL PRIVILEGES ON airflow.* to 'airflow'@'%' WITH GRANT OPTION;
mysql> flush privileges;
```

* Restart MySQL
```
$ sudo service mysql restart
```

### Deploy
* Initialize the Database
```
$ airflow initdb
```
```
├── airflow.cfg
├── airflow.db
├── dags # <--- You have to put your conjob in this folder.
│   ├── bookingInfo.py
│   ├── hbaseTool.py
│   └── pttArticle.py
├── logs
│   └── scheduler
├── requirements.txt
├── tasks
│   └── ptt.py
└── unittests.cfg
```
> The above command will automatically create dags, logs, airflow.db, airflow.cfg and unittests.cfg.

* Configure Airflow Variables
```
$ vim airflow.cfg
```
```
AIRFLOW_CONFIG=/root/DataPipeline/airflow.cfg
AIRFLOW_HOME=/root/DataPipeline
PYTHONPATH=/root/DataPipeline

C_FORCE_ROOT=true

AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Taipei
AIRFLOW__CORE__LOAD_EXAMPLES=False

# celery
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CELERY_BROKER_URL=redis://localhost:6379/1
AIRFLOW__CELERY_RESULT_BACKEND=redis://localhost:6379/2

# mysql
AIRFLOW__CORE__SQL_ALCHEMY_CONN=mysql://airflow:airflow@localhost:3306/airflow
SQLALCHEMY_POOL_RECYCLE=500
```


### Start Airflow
```
$ airflow upgradedb

$ source $AIRFLOW_HOME/env/bin/activate && airflow webserver -p 8080
$ source $AIRFLOW_HOME/env/bin/activate && airflow worker
$ source $AIRFLOW_HOME/env/bin/activate && airflow scheduler
```

### Airflow UI
* http://127.0.0.1:8080/admin
![webserver](https://img.onl/nZLxcR)
![task](https://img.onl/axzMXr)

### Test Tasks
```
$ export AIRFLOW_HOME="$(pwd)"
$ export PYTHONPATH="$(pwd)"
$ airflow test HotArticle crawlPTT 2020-12-02
$ airflow test HotArticle ceateTable 2020-12-02
```

### Use systemctl to start airflow service
You can refer https://github.com/apache/airflow/tree/master/scripts/systemd


> ##### Reference
> * https://github.com/DansProjects/airflow-averageface
> * https://leemeng.tw/a-story-about-airflow-and-data-engineering-using-how-to-use-python-to-catch-up-with-latest-comics-as-an-example.html