# to print .json output, call: scrapy runspider most_wanted.py -o criminals.json

import scrapy
from scrapy.exporters import JsonItemExporter

class scrape(scrapy.Spider):
    name = 'Most Wanted'
    start_urls = ['https://www.nationalcrimeagency.gov.uk/most-wanted-search']
    
    def parse(self, response):
        suspect = response.css("div.span4")
        criminals = suspect.xpath("//div[@class='pull-none item-image']/a/@href")
        yield response.follow_all(response.css('.pagination'))
        yield from response.follow_all(criminals, self.parse_criminal)

    def parse_criminal(self, response):
        def extract_with_css(query):
                return response.css(query).get(default='').strip()

        def look_for_field(field_name):
            try: 
                response.css('.field-value::text').extract()[response.css('.field-label::text').extract().index(field_name)]
                return response.css('.field-value::text').extract()[response.css('.field-label::text').extract().index(field_name)]
            except Exception:
                return "n/a"

        yield { 
            'firstname': response.url.split('/')[-1].split('-')[0], 
            'lastname' : response.url.split('/')[-1].split('-')[1],
            "location": look_for_field("Location: "),
            "about": {
                        "date-of-incident": look_for_field("Date of Incident: "),
                        "crime": look_for_field("Crime: "),
                        "sex": look_for_field("Sex: ")
                    }
        }