from airflow.hooks.mysql_hook import MySqlHook
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# MySQL config
mysqlhook = MySqlHook(mysql_conn_id = 'PTT')

engine_kwargs = {'connect_args': {'charset': 'utf8mb4'}}
Session = sessionmaker(bind=mysqlhook.get_sqlalchemy_engine(engine_kwargs))

session = Session()


def upsert(row, table):
    url = row['url']
    hits = row['hits']
    title = row['title']
    board = row['board']
    author = row['author']
    posted_date = row['timestamp'].split('T')[0]
    description = row['description']

    record = session.query(table).filter_by(title=title, author=author, board=board, url=url).first()
    
    if not record:
        record = table()

    record.url = url
    record.hits = hits
    record.title = title
    record.author = author
    record.board = board
    record.posted_date = datetime.strptime(posted_date, '%Y-%m-%d')
    record.description = description

    session.merge(record)
    session.commit()


def create_table(tablename):
    connection = mysqlhook.get_conn()
    mysqlhook.set_autocommit(connection, True)
    cursor = connection.cursor()

    sql = """CREATE TABLE IF NOT EXISTS `{}` (
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `title` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
          `author` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
          `board` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
          `hits` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
          `url` varchar(4096) COLLATE utf8mb4_unicode_ci NOT NULL,
          `posted_date` timestamp COLLATE utf8mb4_unicode_ci NOT NULL,
          `description` varchar(4096) COLLATE utf8mb4_unicode_ci NOT NULL,
          `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""".format(tablename)

    cursor.execute(sql)
    cursor.close()