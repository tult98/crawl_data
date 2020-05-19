import scrapy
from ..items import ReviewItem
import json


def url_company(): 

    urls = []

    with open('companies.json', 'r', encoding="utf-8") as data_file: 
        data = json.load(data_file)
        # dictionary for saving url and id_company
        d = {}
        for item in data:
            d['url'] = item['url']
            d['id'] = item['id_company']
            urls.append(d)
    
    return urls


class ReviewSpider(scrapy.Spider): 

    name = 'reviews'
    urls = url_company()

    allowed_domains = [
        'reviewcongty.com',
    ]

    start_urls = [
        'https://reviewcongty.com/' + d['url'] for d in urls
    ]

    def parse(self, response):

        reviews = response.xpath('//section[@class="full-reviews"]/div[@class="review card"]')
        company_name = response.css('div.company-info div.company-info__detail h2 a::text').get().strip()

        for review in reviews:

            r = ReviewItem()

            id_review = review.css('div.card-content div.content div').attrib['id'].replace('review_', '')
            reviewer_name = review.css('header.card-header').xpath('./p[@class="card-header-title"]/text()').get().strip()
            review_content = review.css('div.card-content div.content div').xpath('string(./span)').get()
            liked = review.css('footer.card-footer').xpath('./span[@data-id=$val and @data-reaction="LIKE"]/text()', val=id_review).get().strip()
            disliked = review.css('footer.card-footer').xpath('./span[@data-id=$val and @data-reaction="HATE"]/text()', val=id_review).get().strip()

            # calculate rating
            stars = review.css('header.card-header').xpath('./p[@class="card-header-title"]/span/span')
            rating_point = 0
            for star in stars:
                class_name = star.css('i::attr(class)').get()
                if class_name == "fas fa-star":
                    rating_point += 1 
                elif class_name == "fas fa-star-half-alt":
                    rating_point += 0.5

            r['company_name'] = company_name
            r['id_review'] = id_review
            r['reviewer_name'] = reviewer_name
            r['content'] = review_content
            r['rating'] = rating_point
            r['liked'] = liked
            r['disliked'] = disliked

            yield r

        total_pages = response.css('span.pagination-summary b::text').getall()[1]

        if int(total_pages) > 0:
            for page in range(2, int(total_pages)):
                yield response.follow('?tab=latest&page=' + str(page), callback=(self.parse))

