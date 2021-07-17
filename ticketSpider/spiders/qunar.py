import re
import json
from scrapy import Request
import scrapy
from ticketSpider.items import TicketspiderItem

class QunarSpider(scrapy.Spider):
    basesite = 'https://piao.qunar.com'
    name = 'qunar'
    allowed_domains = ['piao.qunar.com']
    start_urls = ['https://piao.qunar.com/ticket/list.htm?keyword=shijiazhuang']

    def parse(self, response):
        sight_items = response.css('#search-list .sight_item')
        for sight_item in sight_items:
            item = TicketspiderItem()
            item['id'] = sight_item.css('::attr(data-id)').extract_first()
            item['area'] = sight_item.css('::attr(data-districts)').extract_first()
            item['address'] = sight_item.css('::attr(data-address)').extract_first()
            item['point'] = sight_item.css('::attr(data-point)').extract_first()
            item['sight'] = sight_item.css('::attr(data-sight-name)').extract_first()
            item['level'] = sight_item.css('.level::text').extract_first()
            item['price'] = sight_item.css('.sight_item_price em::text').extract_first()
            item['count'] = sight_item.css('::attr(data-sale-count)').extract_first()
            item['intro'] = sight_item.xpath(".//div[@class='intro color999']/@title").extract_first()
            item['img_url'] = sight_item.css('::attr(data-sight-img-u-r-l)').extract_first()
            item['detail_url'] = self.basesite + sight_item.xpath(".//h3[@class='sight_item_caption']/a/@href").extract_first()
            if item["detail_url"]:
                # 请求详情页
                yield scrapy.Request(
                    item["detail_url"],
                    callback=self.parse_detail,
                    meta={"item": item}
                )
        #翻页
        #next_url = response.css('.next::attr(href)').extract_first()
        #if next_url:
        #    next_url = "https://piao.qunar.com" + next_url
        #    yield scrapy.Request(
        #        next_url,
        #        callback=self.parse
        #    )

    # 解析详情页
    def parse_detail(self, response):
        item = response.meta["item"]
        item["score"] = response.xpath("//span[@id='mp-description-commentscore']/span/text()").extract_first()
        # 获取详情页的内容、图片
        desc = ''.join(response.xpath("//div[@class = 'mp-charact-intro']//text()").extract())
        item["desc"] = desc.strip()
        item["pic_url"] = ''.join(response.xpath("//div[@class ='mp-description-image']/img/@src").extract())
        item["open_time"] = ''.join(response.xpath("//div[@class = 'mp-charact-time']//text()").extract()).strip()
        item["tips"] = ''.join(response.xpath("//div[@class = 'mp-littletips-desc']//text()").extract()).strip()
        item["traffic"] = ''.join(response.xpath("//div[@class = 'mp-traffic-transfer']//text()").extract()).strip()
        url = "https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=" + item['id'] + \
              "&index=1&page=1&pageSize=10&tagType=0"
        yield Request(url=url, callback=self.parse_comment_request, meta={"item": item})

    def parse_comment_request(self, response):
        item = response.meta["item"]
        myjson = json.loads(response.text)
        total_comment = ""
        for comment in myjson["data"]["commentList"]:
            total_comment += comment["content"]
        item["comment"] = total_comment
        # total_comment里面存的是string 要新建一个comment域，比如item["comment"]
        yield item  # 对返回的数据进行处理

