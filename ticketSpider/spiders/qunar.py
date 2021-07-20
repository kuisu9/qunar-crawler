import json
from scrapy import Request
import scrapy
from ticketSpider.items import TicketspiderItem
import demjson
from scrapy_redis.spiders import RedisCrawlSpider

class QunarSpider(scrapy.Spider):
    basesite = 'https://piao.qunar.com'
    name = 'qunar'
    allowed_domains = ['piao.qunar.com']
    start_urls = [#'https://piao.qunar.com/ticket/list.htm?keyword=北京&region=&from=mpl_search_suggest&sort=pp&page=1',
                  #'https://piao.qunar.com/ticket/list.htm?keyword=河北&region=&from=mpl_search_suggest&sort=pp&page=1',
                  #'https://piao.qunar.com/ticket/list.htm?keyword=浙江&region=&from=mpl_search_suggest&sort=pp&page=1',
                  #'https://piao.qunar.com/ticket/list.htm?keyword=广东&region=&from=mpl_search_suggest&sort=pp&page=1',
                  #'https://piao.qunar.com/ticket/list.htm?keyword=广西&region=&from=mpl_search_suggest&sort=pp&page=1',
                  'https://piao.qunar.com/ticket/list.htm?keyword=山东&region=&from=mpl_search_suggest&sort=pp&page=1']
    #redis_key = 'Ticketspider:start_urls'

    def parse(self, response):
        sight_items = response.css('#search-list .sight_item')
        for sight_item in sight_items:
            item = TicketspiderItem()
            item['id'] = sight_item.css('::attr(data-id)').extract_first()
            item['area'] = sight_item.css('::attr(data-districts)').extract_first()
            item['address'] = sight_item.css('::attr(data-address)').extract_first()
            point = sight_item.css('::attr(data-point)').extract_first()
            item['lon'] = float(point.split(',')[0])
            item['lat'] = float(point.split(',')[1])
            item['sight'] = sight_item.css('::attr(data-sight-name)').extract_first()
            item['level'] = sight_item.css('.level::text').extract_first()
            item['price'] = sight_item.css('.sight_item_price em::text').extract_first()
            item['count'] = sight_item.css('::attr(data-sale-count)').extract_first()
            item['intro'] = sight_item.xpath(".//div[@class='intro color999']/@title").extract_first()
            item['img_url'] = sight_item.css('::attr(data-sight-img-u-r-l)').extract_first()
            detail_url = self.basesite + sight_item.xpath(".//h3[@class='sight_item_caption']/a/@href").extract_first()
            if detail_url:
                # 请求详情页
                yield scrapy.Request(
                    detail_url,
                    callback=self.parse_detail,
                    meta={"item": item}
                )

        #翻页
        #next_url = response.css('.next::attr(href)').extract_first()
        next_url = response.xpath("//a[@class='next']/@href").extract_first()
        if next_url:
            next_url = "https://piao.qunar.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    # 解析详情页
    def parse_detail(self, response):
        item = response.meta["item"]
        item["score"] = response.xpath("//span[@id='mp-description-commentscore']/span/text()").extract_first()
        # 获取详情页的内容、图片
        desc = ''.join(response.xpath("//div[@class = 'mp-charact-intro']//text()").extract())
        item["desc"] = desc.strip()
        item["pic_url"] = (''.join(response.xpath("//div[@class ='mp-description-image']/img/@src").extract())).split('https://')
        item["pic_url"].remove('')
        item["open_time"] = ''.join(response.xpath("//*[@id='mp-charact']/div//div[@class='mp-charact-time']/div/div[@class='mp-charact-desc']/p/text()").extract()).strip()
        item["open_time"] = item["open_time"].replace('；', '；\n')
        item["tips"] = ''.join(response.xpath("//*[@id='mp-charact']/div[@class='mp-charact-littletips']//div[@class='mp-littletips-item']//text()").extract()).strip()
        item["tips"] = (((item["tips"].replace(' ','')).replace('\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n','kk')).replace('\r\n\r\n\r\n\r\n\r\n',':'))
        item['tips'] = ((item["tips"].replace(':',':\n')).replace('；','；\n'))
        item["tips"] = item["tips"].split('kk')
        item["traffic"] = (''.join(response.xpath("//*[@id='mp-traffic']/div[@class='mp-traffic-transfer']//text()").extract()).strip())
        item["traffic"] = (((item["traffic"].replace(' ', '')).replace('\r\n\r\n\r\n\r\n', 'kk')).replace('\r\n\r\n', ':'))
        item['traffic'] = ((item["traffic"].replace(':', ':\n')).replace('；', '；\n'))
        item["traffic"] = item["traffic"].split('kk')
        url = "https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=" + item['id'] + \
              "&index=1&page=1&pageSize=10&tagType=0"
        yield Request(url=url, callback=self.parse_comment_request, meta={"item": item})

    def parse_comment_request(self, response):
        item = response.meta["item"]
        myjson = json.loads(response.text)
        # total_comment里面存的是string 要新建一个comment域，比如item["comment"]
        item["comment"] = ""
        for comment in myjson["data"]["commentList"]:
            item["comment"] += comment["content"]
        item["tag"] = ""
        item["total"] = item["praise"] = item["medium"] = item["critic"] = 0
        for tag in myjson["data"]["tagList"]:
            if tag["tagType"] != 0 and tag["tagType"] != 1 and tag["tagType"] != 2 and tag["tagType"] != 3:
                item["tag"] += tag["tagName"]
            if tag["tagType"] == 0:
                item["total"] = tag["tagNum"]
            if tag["tagType"] == 1:
                item["praise"] = tag["tagNum"]
            if tag["tagType"] == 2:
                item["medium"] = tag["tagNum"]
            if tag["tagType"] == 3:
                item["critic"] = tag["tagNum"]
        url = "https://piao.qunar.com/ticket/detail/recommendSight.json?sightId=" + item['id'] + "&longitude=" + str(item["lon"]) + "&latitude=" + str(item["lat"])
        yield Request(url=url, callback=self.parse_recommend_request, meta={"item": item})

    def parse_recommend_request(self, response):
        item = response.meta["item"]
        recommendjson = json.loads(response.text)
        item["recommend"] = ""
        for recommend in recommendjson["data"]:
            item["recommend"] += recommend["id"] + ","
        item["recommend"] = item["recommend"].split(',')
        item["recommend"].remove('')
        item["recommend1"] = recommendjson["data"][0]
        item["recommend2"] = recommendjson["data"][1]
        item["recommend3"] = recommendjson["data"][2]
        item["recommend4"] = recommendjson["data"][3]
        item["recommend5"] = recommendjson["data"][4]
        item["recommend6"] = recommendjson["data"][5]
        item["recommend7"] = recommendjson["data"][6]
        item["recommend8"] = recommendjson["data"][7]

        #url = "https://piao.qunar.com/ticket/detail/getTickets.json?sightId=" + item['id']
        #yield Request(url=url, callback=self.parse_ticket_request, meta={"item": item})

    #def parse_ticket_request(self, response):
        #item = response.meta["item"]
        #ticketjson = json.loads(response.text)
        #item["ticket"] = {}
        #item["ticket"] = ticketjson["data"]["recommendTicketList"]
        yield item  # 对返回的数据进行处理


