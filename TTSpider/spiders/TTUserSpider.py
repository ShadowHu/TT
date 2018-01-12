#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-12 13:30:47
# @Author  : Shadow Hu (shadow_hu1441@163.com)
# @GitHub    : https://github.com/ShadowHu

import scrapy
# from scrapy.loader import ItemLoader
from TTSpider.items import TTUserspiderItem
from scrapy import Request

DOMAIN = "https://twitter.com"
AL =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class TTUserSpider(scrapy.Spider):
    name = "ttuser"
    start_urls = ["https://twitter.com/i/directory/profiles/{}".format(x) for x in list(range(1,27)) + AL]
    allowed_domains = ["twitter.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'TTSpider.pipelines.TTSpiderPipeline':  400
        }
    }

    # https://twitter.com/i/directory/profiles
    def parse(self, response): 
        rows = response.xpath('//div[@class="directory-page"]/div[@class="row"]//a')
        screenname = response.xpath('//span[@class="screenname"]')
        if screenname:
            for row in rows:
                item = TTUserspiderItem()
                item['url'] =  DOMAIN + row.xpath('@href').extract()[0]
                item['name'] = row.xpath('span[@class="screenname"]/text()').extract()[0]
                return item
        else:
            for row in rows:
                # print(row.xpath('@href').extract())
                yield Request(DOMAIN + row.xpath('@href').extract()[0], callback=self.parse)

    # def  parse1(self, response):
    #     pass