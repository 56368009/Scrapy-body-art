# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtItem(scrapy.Item):
    # 主题标题
    title = scrapy.Field()
    #主题url
    url = scrapy.Field()

    # 主题标题
    suburl = scrapy.Field()
    # 每个页面链接
    pageulr = scrapy.Field()
    # 图片地址
    image = scrapy.Field()
    # 图片名字
    name  = scrapy.Field()

    # 图片路径
    file = scrapy.Field()


