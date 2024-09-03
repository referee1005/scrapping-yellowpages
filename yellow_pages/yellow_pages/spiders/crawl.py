# -*- coding: utf-8 -*-
from itertools import count
import scrapy
import csv

DOMAIN_NAME = 'www.yellowpages.com'
terms = 'dentist'
location = 'Newyork'


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = [DOMAIN_NAME]

    start_urls = []

    def __init__(self,
                 param1='restaurant',
                 param2='NewYork',
                 count=1,
                 *args,
                 **kwargs):
        super(CrawlSpider, self).__init__(*args, **kwargs)
        # self.start_urls = 'https://' + DOMAIN_NAME + '/search?search_terms=' + param1 + '&geo_location_terms=' + param2
        self.param1 = param1
        self.param2 = param2
        self.count = count
        self.data = []
        self.iterator = 0
        # self.start_requests()

    def start_requests(self):
        url = 'https://' + DOMAIN_NAME + '/search?search_terms=' + self.param1 + '&geo_location_terms=' + self.param2
        print('navigate to ', url)
        yield scrapy.Request(url=url,
                             callback=self.parse,
                             meta={'dont_obey_robotstxt': True})

    def parse(self, response):
        for listing in response.css('.search-results .v-card'):
            self.iterator += 1
            name = listing.css('.business-name span::text').get()
            phone = listing.css('.phones.phone.primary::text').get()
            address = ' '.join(listing.css('.street-address::text').getall())
            history = listing.css('.years-in-business strong::text').get()
            print(name, phone, address, history)
            self.data.append({
                'name': name,
                'phone': phone,
                'address': address,
                'history': history
            })

        # Pagination - assuming there's a 'Next' button to follow

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None and self.iterator <= int(self.count):
            yield response.follow(next_page,
                                  callback=self.parse,
                                  meta={'dont_obey_robotstxt': True})
        else:
            self.save_data()

    def save_data(self):
        # Save scraped data to a file (e.g., JSON)
        filename = f'{self.param1}_{self.param2}_results.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'phone', 'address', 'history']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.data:
                writer.writerow(item)
        self.log(f'Saved data to {filename}')

    def closed(self, reason):
        # This method is called when the spider is closed
        return {
            'status': 'completed',
            'param1': self.param1,
            'param2': self.param2,
            'data': self.data
        }
