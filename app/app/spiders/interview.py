import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

from time import sleep

START_URL = 'https://forms.gle/s8ME2PMP9o5PMKsW7' 

class InterviewSpider(scrapy.Spider):
    name = 'interview'
    allowed_domains = [START_URL]
    start_urls = [START_URL]

    def start_requests(self):
        yield SeleniumRequest(url=START_URL, callback=self.parse_1st_page_review)

    def parse_1st_page_review(self, responce):
        driver = responce.meta['driver']

        sleep(2)
        driver.find_element_by_css_selector('div[data-value="English language"]').click()
        sleep(2)
        driver.find_element_by_css_selector('div[data-is-receipt-checked] div[role="button"]').click()
        sleep(2)

        self.parse_2nd_page_review(driver)

    def parse_2nd_page_review(self, driver):
        driver.find_element_by_css_selector('input[aria-labelledby="i1"]').send_keys('Николай')
        import ipdb; ipdb.set_trace()
        pass