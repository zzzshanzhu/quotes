import pymongo
import pymysql
from scrapy.exceptions import DropItem

class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class MySQLPipeline(object):
    def __init__(self, mysql_url,mysql_port,mysql_db,mysql_username,mysql_password,):
        self.mysql_url = mysql_url
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db
        self.mysql_username = mysql_username
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get('MYSQL_URL'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_db = crawler.settings.get('MYSQL_DB'),
            mysql_username = crawler.settings.get('MYSQL_USERNAME'),
            mysql_password = crawler.settings.get('MYSQL_PASSWORD')
        )

    def open_spider(self, spider):
        self.con = pymysql.connect(
            host=self.mysql_url,
            port=self.mysql_port,
            db=self.mysql_db,
            user=self.mysql_username,
            password=self.mysql_password,
            charset='utf8',
            use_unicode=True)
        self.cue = self.con.cursor();
        self.con.autocommit(True)

    def process_item(self, item, spider):


        try:
            self.cue.execute("insert into quotestoscrape (text,author,tags) values (%s,%s,%s);",
                        [item['text'], item['author'], str(item['tags'])])
            print("Mysql insert success")  # 测试语句
        except Exception as e:
            print('Insert error:', e)
            self.con.rollback()
        else:
            self.con.commit()
        return item

    def close_spider(self, spider):
        self.cue.close()
        self.con.close()