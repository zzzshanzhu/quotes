# -*- coding: utf-8 -*-
import scrapy
import json
from quotes.items import QuotesItem

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    count = None

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)

        print('正在爬取'+next+'个页面：'+url)
        yield scrapy.Request(url = url,callback = self.parse)
