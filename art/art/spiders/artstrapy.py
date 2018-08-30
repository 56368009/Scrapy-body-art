__author__ = 'LinYi'
__date__ = '18/8/16 15:59'
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from art.items import ArtItem
from scrapy.http import Request
import os, re


class ArtScrapy(Spider):
    startlist = []
    name = 'art'
    next = 1
    max_next = 0
    urls = 'http://www.xixirenti.cc/'
    allow_domnains = ["http://www.xixirenti.cc"]
    start = 'http://www.xixirenti.cc/zhongguo/list_2_1.html'
    start_urls = ['http://www.xixirenti.cc/zhongguo/list_2_' + str(next) + '.html', ]

    def parse(self, response):
        # 获取最大页数
        if self.max_next == 0:

            temp_next =  response.xpath('/html/body/div/div[10]/ul/li[14]/a/@href').extract()[0]
            self.max_next = int(re.findall(r"\d+\.?\d*",temp_next)[-1].replace('.', ''))
        for i in response.xpath('/html/body/div/div[8]/div/ul/li[*]'):
            itme = ArtItem()
            itme['title'] = i.xpath('./a/img/@alt').extract()[0]
            itme['url'] = i.xpath('./a/@href').extract()[0]
            self.startlist.append(itme)

        # 爬取所有主题内容
        for list in self.startlist:
            title = list['title']
            url = list['url']
            # 访问
            url_s = self.urls + url
            # 给每个主题发送请求
            yield Request(url_s, self.son_url, meta={'meta_1': title})

        # 判断页数
        if self.next < self.max_next:
            # 翻页
            self.next += 1
            next_url = 'http://www.xixirenti.cc/zhongguo/list_2_' + str(self.next) + '.html'
            yield self.scrapy.Request(next_url, self.parse)

    def son_url(self, response):
        sonlist = []
        resurl = response.url[0:-5]
        # 获取图片标题
        title = response.meta['meta_1']
        # 翻页默认值
        next_2 = 1
        numb_url = response.xpath('//*[@id="body"]/div/div[9]/ul/li[1]/a/text()').extract()[0]
        # 最大页数
        numb = re.findall(r"\d+\.?\d*", numb_url)
        # 创建文件夹
        File = './data/' + title
        if (not os.path.exists(File)):
            os.makedirs(File)
        # 翻页 获取每页数据
        for i in range(int(numb[0])):
            # 2410_2.html
            # 是否第一次循环
            if next_2 == 1:
                # 第一页
                item = ArtItem()
                # 页面url
                item['pageulr'] = resurl + '.html'
                # 存储路径
                item['file'] = File
                sonlist.append(item)
                next_2 += 1
            else:
                strurl = resurl + '_' + str(next_2) + '.html'
                item = ArtItem()
                # 页面url
                item['pageulr'] = strurl
                # 存储路径
                item['file'] = File
                sonlist.append(item)

                next_2 += 1

        # 遍历sonlist访问每一个链接
        for s in sonlist:

            yield Request(s['pageulr'], callback=self.getimage, meta={'meta_2': s['file']})


    def getimage(self, response):
        lujing = response.meta['meta_2']
        # 获取图片
        item = ArtItem()
        mage = response.xpath('//*[@id="body"]/div/div[8]/a[2]/@href').extract()[0]
        pro  = 'http://www.xixirenti.cc' + mage
        item['image'] = pro
        item['file'] = lujing
        item['name'] = str(hash(pro))


        yield item
