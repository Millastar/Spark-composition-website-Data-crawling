# -*- coding: utf-8 -*-
import scrapy
from NewsData.items import NewsdataItem
from bs4 import BeautifulSoup
from urllib import parse
from gerapy_auto_extractor.extractors import *


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = []
    start_urls = [
        ['https://www.easyzw.com/html/xieren/', '作文题材', '写人'],
        ['https://www.easyzw.com/html/xiejing/', '作文题材', '写景'],
        ['https://www.easyzw.com/html/xiangxiang/', '作文题材', '想象'],
        ['https://www.easyzw.com/html/dongwuzuowen/', '作文题材', '动物'],
        ['https://www.easyzw.com/html/zhouji/', '作文题材', '周记'],
        ['https://www.easyzw.com/html/yingyuzuowen/', '作文题材', '英语'],
        ['https://www.easyzw.com/html/huanbaozuowen/', '作文题材', '环保'],
        ['https://www.easyzw.com/html/xinqing/', '作文题材', '心情'],
        ['https://www.easyzw.com/html/zhuangwuzuowen/', '作文题材', '状物'],
        ['https://www.easyzw.com/html/riji/', '作文题材', '日记'],
    ]

    def start_requests(self):
        for url in self.start_urls: #不止爬一个网站，所以要循环，self是调用自身的意思
            item = NewsdataItem()
            item["site"] = url[1]
            item["item"] = url[2]
            item["student_id"] = "20201905"
            # ['http://www.news.cn/politicspro/', '新华网', '时政']

            yield scrapy.Request(url=url[0], meta={"item": item}, callback=self.parse) #yield是返回函数，url是目标网址，callback是函数处理方式

    def parse(self, response):
        item = response.meta["item"]

        site_ = item["site"]
        item_ = item["item"]
        title_list = response.xpath('//li/a/text()').extract() #xpath的解析方式，要从网站的开发者模式查看，extract表示解析成列表的方式
        url_list = response.xpath('//li/a/@href').extract() #双斜杠表示模糊匹配

        # date_list = response.xpath(
        #     '//*[@id="content-list"]/div/div[@class="txt"]/div[@class="info clearfix domPc"]/div[@class="time"]/text()').extract()

        # print(len(title_list), len(url_list), len(date_list))
        # item = response.meta["item"]
        # print(item)


            # print(url_list)
        for each in range(len(title_list)): #取随便哪一个的长度
            item = NewsdataItem()  #定义字典
            item["title"] = title_list[each] #然后开始向里面填充，注意这里面的名字要和items里的一样
            item["url"] = "https://www.easyzw.com" + str(url_list[each]) #这一步是相对路径改成绝对路径，有些网站不用改
            item["site"] = site_
            item["item"] = item_
            item["student_id"] = "20201905"
            # data = extract_list(response.text)
            # data = extract_list(response.text)
            yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_detail) #这是访问这个循环体内的url，相当于点击操作，处理方法为下面的parse_detail
            #meta表示带着已经填充好的url数据

        # for each in range(len(data)):
        #     # item = NewsdataItem()
        #     item = response.meta["item"]
        #     item["title"] = data[each]["title"]
        #     item["url"] = parse.urljoin(response.url, data[each]["url"])
        #     yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_detail)

    def parse_detail(self, response):
        # data = extract_detail(response.text)
        item = response.meta["item"]  #重新定义一个字典
        item["date"] = ""
        strs = response.xpath('//div[@class="content"]').extract_first() #和上面一样从开发者模式定位，first是因为列表无法存入字典
        item["content"] = BeautifulSoup(strs, 'lxml').text
        return item #把数据写入MongoDB里
