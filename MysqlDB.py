import pymysql

MYSQL_URL = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'quotestoscrape'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'

mysql_url=MYSQL_URL
mysql_port=MYSQL_PORT
mysql_db = MYSQL_DB
mysql_username = MYSQL_USERNAME
mysql_password = MYSQL_PASSWORD

con = pymysql.connect(
    host=mysql_url,
    port=mysql_port,
    user=mysql_username,
    passwd=mysql_password,
    db=mysql_db,
    charset='utf8',
    use_unicode=True)

con.autocommit(True)

cue = con.cursor()
print('链接成功')
for i in range(10):
    print('插入数据...')
    cue.execute('insert into quotestoscrape (text,author,tags) values ("a","b","c");')
    con.commit()
con.close()