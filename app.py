from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawl_data.spiders.company_spider import CompanySpider
from crawl_data.spiders.reviews_spider import ReviewSpider

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl(ReviewSpider)
    process.start()