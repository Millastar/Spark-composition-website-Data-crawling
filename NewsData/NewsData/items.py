# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsdataItem(scrapy.Item):
    title=scrapy.Field() #文章标题
    url=scrapy.Field() #文章链接
    date=scrapy.Field() #发布日期
    content=scrapy.Field() #文章正文
    site=scrapy.Field() #站点
    item=scrapy.Field() #栏目
    student_id=scrapy.Field() #学号

