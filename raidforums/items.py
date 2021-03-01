# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RaidforumsItem(scrapy.Item):
    category = scrapy.Field()
    sub_category = scrapy.Field()
    forum_name = scrapy.Field()
    forum_description = scrapy.Field()
    forum_link = scrapy.Field()
    threads_count = scrapy.Field()
    posts_count = scrapy.Field()
    forum_last_post = scrapy.Field()
