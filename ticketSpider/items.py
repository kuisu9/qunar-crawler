# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from ticketSpider.elasticsearch_orm import qunarType



class TicketspiderItem(scrapy.Item):
    id = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    sight = scrapy.Field()
    level = scrapy.Field()
    price = scrapy.Field()
    count = scrapy.Field()
    intro = scrapy.Field()
    img_url = scrapy.Field()
    score = scrapy.Field()
    desc = scrapy.Field()
    open_time = scrapy.Field()
    tips = scrapy.Field()
    traffic = scrapy.Field()
    pic_url = scrapy.Field()
    comment = scrapy.Field()
    tag = scrapy.Field()
    total = scrapy.Field()
    praise = scrapy.Field()
    medium = scrapy.Field()
    critic = scrapy.Field()
    recommend = scrapy.Field()
    recommend1 = scrapy.Field()
    recommend2 = scrapy.Field()
    recommend3 = scrapy.Field()
    recommend4 = scrapy.Field()
    recommend5 = scrapy.Field()
    recommend6 = scrapy.Field()
    recommend7 = scrapy.Field()
    recommend8 = scrapy.Field()
    #ticket = scrapy.Field()

    def save_to_es(item):
        qunar = qunarType()
        qunar.id = item['id']
        qunar.area = item['area']
        qunar.address = item['address']
        qunar.lon = item['lon']
        qunar.lat = item['lat']
        qunar.sight = item['sight']
        qunar.level = item['level']
        qunar.price = item['price']
        qunar.count = item['count']
        qunar.intro = item['intro']
        qunar.img_url = item['img_url']
        qunar.score = item['score']
        qunar.desc = item['desc']
        qunar.open_time = item['open_time']
        qunar.tips = item['tips']
        qunar.traffic = item['traffic']
        qunar.pic_url = item['pic_url']
        qunar.comment = item['comment']
        qunar.tag = item['tag']
        qunar.total = item['total']
        qunar.praise = item['praise']
        qunar.medium = item['medium']
        qunar.critic = item['critic']
        qunar.recommend = item['recommend']
        qunar.recommend1 = item['recommend1']
        qunar.recommend2 = item['recommend2']
        qunar.recommend3 = item['recommend3']
        qunar.recommend4 = item['recommend4']
        qunar.recommend5 = item['recommend5']
        qunar.recommend6 = item['recommend6']
        qunar.recommend7 = item['recommend7']
        qunar.recommend8 = item['recommend8']
        #qunar.ticket = item['ticket']
        qunar.save()
        return
    pass
