#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-12 13:30:47
# @Author  : Shadow Hu (shadow_hu1441@163.com)
# @GitHub    : https://github.com/ShadowHu

import scrapy
# from scrapy.loader import ItemLoader
from TTSpider.items import TTUserspiderItem
from scrapy import Request
import json, time
from lxml import etree
import logging
import gc


from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='{}.txt'.format(int(time.time())),
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)


logger = logging.getLogger(__name__)

DOMAIN = "https://twitter.com/"
AL =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
URL = "https://twitter.com/i/search/timeline?vertical=default&q=a&src=typd&composed_count=0&include_available_features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count={}&min_position={}"

class TTUserSpider(scrapy.Spider):
    name = "ttuser"
    # start_urls = ["https://twitter.com/i/directory/profiles/{}".format(x) for x in list(range(1,27)) + AL]
    start_urls = ["https://twitter.com/i/search/timeline?vertical=default&q=a&src=typd&composed_count=0&include_available_features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count=0&min_position=TWEET--953615938338938881-BD1UO2FFu9QAAAAAAAAVfAAAAAcAAABWAAAARAAAAAAAAAAgAAAAAAACAAAAAIAAAAAAAAAAAAAAAAAAAIACQAAABAAAQEAAAAAAAAAAAAAAAAAAAAAAAAICAIEQAABAAQAAAAAAQAAAAAAIAAAAgABAAAAAAAAAAEAAAAABAAAAAAAAAAAAACQAAAAAAAAQAACAAAAAAAEAAAAAAAAAAQAAAAAAAAAAAAAAEAAAAAAAAAEAMAAAAAAAAAABAAAAAAAAAAAAAgAAAAAAAAgAAAIBAAEAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAAAAAAAAADAAAAIAAEAAAAAAAAAAAAAAAAAQAAAAAAAgAAAAACIAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAARACEAAAAAACACAAAAAAAAAAAAAAAAAAAIgCQAAgIgEAAAAgYIAAAQAAAAAAAAAAAAAAAAAAAAAAAABAACAAAAAAAQAAAAAAAAAAAEAAAAAQAAEAAAAABAAAAAAAQASAAiAAAEEAAAAAAAQAAAQAAAACQAAAAAAAAAAAIAAAAAAgAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAABAAABAAAAAAAAAACAAAgAAAAAgIAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAQAAAAAAAAQIAAAgAAAAAgQAAAAIABIAAAAgAUiAAAAAAAAAAAAAAAAAAAAAQAIAAAAAAABICAAAAAMAAAgACAAAAAAAAAAAAAAAEAABEACAAAAAAACEAAACAAAAAAAAAAAAAAAgAAAAAAAQAAACAAAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAA%3D%3D-T-0"]
    allowed_domains = ["twitter.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'TTSpider.pipelines.TTSpiderPipeline':  90
        }
    }

    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        items_html = js['items_html']
        min_position = js['max_position']
        new_latent_count = js['new_latent_count']
        nodes = etree.HTML(items_html).xpath("//div[@class='stream-item-header']")
        # print(items_html)
        for node in nodes:
            try:
                item = TTUserspiderItem()
                item['url'] = DOMAIN + node.xpath("a/span[@class='username u-dir u-textTruncate']/b/text()")[0]
                item['name'] = node.xpath("a/span[@class='FullNameGroup']/strong/text()")[0]
            except IndexError:
                logger.error("IndexError: "+item['url'])
            else:
                yield Request(item['url'], callback=self.parse_address, meta={"item":item})

        yield Request(URL.format(new_latent_count, min_position), callback=self.parse)

    def parse_address(self, response):
        item = response.meta['item']
        item['address'] = response.xpath("//span[@class='ProfileHeaderCard-locationText u-dir']//text()")[0].extract()
        return item