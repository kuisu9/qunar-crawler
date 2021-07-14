
from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, analyzer, Completion, Keyword, Text, Integer, Double
from elasticsearch_dsl.connections import connections

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=["127.0.0.1"],timeout=60) # hosts允许连接多个服务器


class qunarType(Document): # 相当于mappings映射
    id = Text()
    area = Text()
    address = Text()
    point = Text()
    sight = Text()
    level = Text()
    price = Integer()
    count = Integer()
    img_url = Text()
    detail_url = Text()
    score = Double()
    desc = Text()

    class Index:
        # 数据库名称和表名称
        name = "qunar"

if __name__ == "__main__":
    qunarType.init()