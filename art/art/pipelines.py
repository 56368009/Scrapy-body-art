# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, urllib


class ArtPipeline(object):

    def process_item(self, item, spider):
        img_url = item['image']
        file = item['file']
        name = item['name']
        try:

            # 是否存在
            if (not os.path.exists((file))):  # xxx是文件夹名称
                # 不存在就创建新的文件夹
                os.makedirs(file)

            # 获得图片后缀
            file_suffix = os.path.splitext(img_url)[1]
            # 拼接图片名（包含路径）
            perfect = file + '/' + name + file_suffix
            if_s = os.path.exists(perfect)
            # 判断文件是否存在存在就不下载了
            if if_s != True:
                # 下载图片，并保存到文件夹中
                urllib.request.urlretrieve(img_url, perfect)
        except IOError as e:
            print
            '文件操作失败', e
        except Exception as e:
            print
            '错误 ：', e
        return item
