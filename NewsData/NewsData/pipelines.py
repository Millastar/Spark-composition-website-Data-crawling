# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 添加必备包和加载设置
import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class NewsdataPipeline:
    # class中全部替换
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DATABASE"]
        sheetname = settings["MONGODB_TABLE"]
        #username = settings["MONGODB_USER"]
        #password = settings["MONGODB_PASSWORD"]
        # 创建MONGODB数据库链接
        #client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        # 数据写入
        self.post.insert_one(data)
        return item

