import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'test'

mongo_url=MONGO_URL
mongo_db=MONGO_DB

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]

print('链接成功')
for i in range(10):
    print('插入数据...')
    data = {'name': 'weihong', 'age': 19}
    db[MONGO_DB].insert(data)

client.close()