import scrapy
from ..items import (
    CompanyItem,
)

class CompanySpider(scrapy.Spider): 
    name = "companies"

    allowed_domains = [
        'reviewcongty.com',
    ]

    start_urls = [
        'https://reviewcongty.com/',
    ]

    def parse(self, response):

        companies = response.css('div.company-item div.company-info div.company-info__detail')

        for company in companies:

            c = CompanyItem()

            company_name = company.css('h2 a::text').get().replace('\n',' ').strip()
            company_url = company.css('h2 a::attr(href)').get()
            company_type = company.xpath('string(//div[@class="company-info__other"]//span[1])').get().replace('\n',' ').strip()
            company_capacity = company.xpath('string(//div[@class="company-info__other"]//span[2])').get().replace('\n',' ').strip()
            company_address = company.xpath('string(//div[@class="company-info__location"])').get().replace('\n',' ').strip()

            # calculate the rating of company 
            stars = company.css('h2 span.company-info__rating span span.has-text-warning')
            rating_point = 0
            for star in stars:
                class_name = star.css('i::attr(class)').get()
                if class_name == "fas fa-star":
                    rating_point += 1 
                elif class_name == "fas fa-star-half-alt":
                    rating_point += 0.5
            
            c['name'] = company_name
            c['url'] = company_url
            c['company_type'] = company_type
            c['capacity'] = company_capacity
            c['address'] = company_address
            c['rating'] = rating_point

            yield c
            

        total_pages = response.css('span.pagination-summary b::text').getall()[1]

        if int(total_pages) > 0:
            for page in range(2, int(total_pages)):
                yield response.follow('?tab=latest&page=' + str(page), callback=(self.parse))