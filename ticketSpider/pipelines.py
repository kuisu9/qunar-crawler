# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .elasticsearch_orm import qunarType
import csv

class TicketspiderPipeline(object):
    def __init__(self):
        self.f = open('ticker.csv', 'w', encoding='utf-8', newline='')
        self.fieldnames = ['id', 'area', 'address', 'point', 'sight', 'level', 'price', 'count', 'intro', 'img_url', 'detail_url','score', 'desc', 'open_time', "tips", "traffic", 'pic_url', 'comment']
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()
    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()

class ElasticsearchPipeline(object):
    #将数据写入到es中
    def process_item(self, item, spider):
        #将item转换为es的数据
        item.save_to_es()
        return item