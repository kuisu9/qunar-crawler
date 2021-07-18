from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, analyzer, Completion, Keyword, Text, Integer, Double, Object
from elasticsearch_dsl.connections import connections

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=["127.0.0.1"],timeout=60) # hosts允许连接多个服务器


class qunarType(Document): # 相当于mappings映射
    id = Keyword()
    area = Text()
    address = Text()
    lon = Double()
    lat = Double()
    sight = Text()
    level = Text()
    price = Double()
    count = Integer()
    intro = Text()
    img_url = Text()
    score = Double()
    desc = Text()
    open_time = Text()
    tips = Text()
    traffic = Text()
    pic_url = Text()
    comment = Text()
    tag = Text()
    total = Integer()
    praise = Integer()
    medium = Integer()
    critic = Integer()
    recommend = Text()
    ticket = Nested()

    class Index:
        # 数据库名称和表名称
        name = "qunar"

if __name__ == "__main__":
    qunarType.init()