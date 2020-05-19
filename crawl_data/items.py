# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CompanyItem(scrapy.Item):
    id_company = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field() 
    company_type = scrapy.Field() 
    capacity = scrapy.Field() 
    address = scrapy.Field() 

class ReviewItem(scrapy.Item):
    id_company = scrapy.Field()
    company_name = scrapy.Field()
    id_review = scrapy.Field()
    reviewer_name = scrapy.Field()
    content = scrapy.Field() 
    rating = scrapy.Field() 
    liked = scrapy.Field() 
    disliked = scrapy.Field() 

class CommentItem(scrapy.Item): 
    comment_id = scrapy.Field()
    commenter_name = scrapy.Field() 
    content = scrapy.Field() 

