# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# This will be a class to represent the data we scrape from the web
class PdfUrlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # These are the only two things we want our scraper to scrape (according to client specifications)
    url         = scrapy.Field()
    filename    = scrapy.Field()

