import scrapy
import re
import time
from scrapy.http import Request

from raidforums.items import RaidforumsItem

class RaidforumSpiderSpider(scrapy.Spider):
    name = 'raidforum_spider'
    allowed_domains = ['raidforums.com/']
    start_urls = ['https://raidforums.com/']
    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br'
    }

    def convert_list_to_string(self, data):
        return ''.join(data).strip()
    

    def parse(self, response):

        data = response.xpath('//*[@id="forum-tabs"]/ul//li')
        for response in data:
            section_url = self.start_urls[0]+response.xpath('a/@href').get()
            section_info = {
                'section_name':response.xpath('string(.)').get().strip().replace(" ",""),
                'tab_lists' :response.css('li::attr(data-easytabs-ids)').get()
            }
            yield Request(section_url, callback=self.parse_category_content, dont_filter=True, meta={'section_info':section_info})
    
    def parse_content(self, category_response, section_name, forum_sub_category=None):
        for response in category_response:
            forum_section = section_name
            forum_sub_category = forum_sub_category if forum_sub_category else None
            forum_link =  self.start_urls[0]+response.xpath('td[2]/a/@href').extract()[0]
            forum_name = response.xpath('td[2]//text()').extract()[1]
            forum_description = response.xpath('td[2]//text()').extract()[3]
            forum_threads_count = response.xpath('td[3]//text()').extract()[1]
            forum_posts_count = response.xpath('td[4]//text()').extract()[1]
            forum_last_post = {
            'forum_last_post_name':response.xpath('td[5]//text()').extract()[3],
            'forum_last_post_user':response.xpath('td[5]//text()').extract()[6],
            'forum_last_post_date':self.convert_list_to_string(response.xpath('td[5]//text()').extract()[7:9])
            }
            item = RaidforumsItem()
            item['category'] = forum_section
            item['sub_category'] = forum_sub_category
            item['forum_link'] = forum_link
            item['forum_name'] = forum_name
            item['forum_description'] = forum_description
            item['threads_count'] = forum_threads_count
            item['posts_count'] = forum_posts_count
            item['forum_last_post'] = forum_last_post

            yield item


    def parse_category_content(self, response):
        
        meta_response_data = response.meta['section_info']
        section_name = meta_response_data['section_name']
        tab_lists = meta_response_data['tab_lists'].split(',')
        if len(tab_lists) >= 2:
            for tab_id in tab_lists:
                forum_sub_category = response.xpath('//*[@id="{0}"]/table/thead/tr/td/strong//text()'.format(tab_id)).get()
                category_response = response.xpath('//*[@id="{0}"]/table/tbody//tr'.format(tab_id))
                yield from self.parse_content(category_response, section_name, forum_sub_category)
        else:
            category_response = response.xpath('//*[@id="{0}"]/table/tbody//tr'.format(tab_lists[0]))
            yield from self.parse_content(category_response, section_name)
            

        
