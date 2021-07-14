

import scrapy
from ticketSpider.items import TicketspiderItem

class QunarSpider(scrapy.Spider):
    basesite = 'https://piao.qunar.com'
    name = 'qunar'
    allowed_domains = ['piao.qunar.com']
    start_urls = ['https://piao.qunar.com/ticket/list.htm']

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
            item['img_url'] = sight_item.css('::attr(data-sight-img-u-r-l)').extract_first()
            item['detail_url'] = self.basesite + sight_item.xpath(".//h3[@class='sight_item_caption']/a/@href").extract_first()
            if item["detail_url"]:
                # 请求详情页
                yield scrapy.Request(
                    item["detail_url"],
                    callback=self.parse_detail,
                    meta={"item": item}
                )
        # 翻页
        next_url = response.css('.next::attr(href)').extract_first()
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
        item["desc"] = response.xpath("//div[@class='mp-charact-desc']/p/text()").extract_first()
        yield item  # 对返回的数据进行处理
