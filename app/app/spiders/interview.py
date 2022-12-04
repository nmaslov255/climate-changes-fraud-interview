import scrapy


class InterviewSpider(scrapy.Spider):
    name = 'interview'
    allowed_domains = ['https://forms.gle/s8ME2PMP9o5PMKsW7']
    start_urls = ['https://forms.gle/s8ME2PMP9o5PMKsW7']

    def parse(self, response):
        pass
