from airflow.hooks.mysql_hook import MySqlHook

from model.PTT import Info

mysqlhook = MySqlHook(mysql_conn_id='PTT')


def upsert(row):
    title = row['title']
    author = row['author']
    board = row['board']
    hits = row['hits']
    url = row['url']
    posted_date = row['timestamp']
    description = row['description']

    record = session.query(Info).filter_by(title=title, author=author, board=board,
                                          url=url).first()
    if not record:
        record = Info()

    record.title = title
    record.author = author
    record.board = board
    record.hits = hits
    record.posted_date = posted_date
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
            """.format(tablename)
    cursor.execute(sql)
    cursor.close()