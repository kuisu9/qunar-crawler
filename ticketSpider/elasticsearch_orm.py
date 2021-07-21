from datetime import datetime
from elasticsearch_dsl import Document, Nested, search, analyzer, analysis, Completion, Keyword, Text, Integer, Double, Object
from elasticsearch_dsl.connections import connections

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=["127.0.0.1"],timeout=60) # hosts允许连接多个服务器

my_pinyin = analysis.token_filter('ik_smart_pinyin',
                                  type = "pinyin",)
ik_smart_pinyin = analyzer('ik_smart_pinyin',
                              type = "custom",
                              tokenizer="ik_smart",
                              filter=[my_pinyin],)
ik_smart = analyzer('ik_smart')

class qunarType(Document): # 相当于mappings映射
    id = Keyword()
    area = Text(analyzer = ik_smart)
    address = Text()
    lon = Double()
    lat = Double()
    sight = Text(analyzer = ik_smart_pinyin)
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
    recommend1 = Nested()
    recommend2 = Nested()
    recommend3 = Nested()
    recommend4 = Nested()
    recommend5 = Nested()
    recommend6 = Nested()
    recommend7 = Nested()
    recommend8 = Nested()
    #ticket = Nested()

    class Index:
        # 数据库名称和表名称
        name = "qunar"

if __name__ == "__main__":
    qunarType.init()