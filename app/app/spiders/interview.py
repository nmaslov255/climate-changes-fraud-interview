import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

from time import sleep
from random import choice

START_URL = 'https://forms.gle/s8ME2PMP9o5PMKsW7'

CITY_KG_RU = ['Айдаркен','Балыкчы','Баткен','Бишкек','Джалал-Абад','Кадамжай','Каинды','Кант','Кара-Балта','Каракол',
              'Кара-Куль','Кара-Суу','Кемин','Кербен','Кок-Джангак','Кочкор-Ата','Кызыл-Кия','Майлуу-Суу','Нарын',
              'Ноокат','Орловка','Ош','Раззаков','Сулюкта','Талас','Таш-Кумыр','Токмок','Токтогул','Узген',
              'Чолпон-Ата','Шопоков']

CITY_KG_EN = ['Header','Fisherman','Batken','Bishkek','Jalal-Abad','Step by step','Cain','Cant','Black-Axe','Caracol',
              'Kara-Kul','Black Water','Min','Caravan','Kok-Jangak','Kochkor-Ata','Kyzyl-Kiya','Oil-Water','Naryn',
              'Nookat','Orlovka','Osh','Razzakov','Sulyukta','Talas','Tash-Kumyr','Knock','Stop','Expired',
              'Cholpon-Ata','Shopokov']

class InterviewSpider(scrapy.Spider):
    name = 'interview'
    allowed_domains = [START_URL]
    start_urls = [START_URL]

    def start_requests(self):
        yield SeleniumRequest(url=START_URL, callback=self.parse_1st_page_review)

    def parse_1st_page_review(self, responce):
        driver = responce.meta['driver']

        sleep(5)
        driver.find_element_by_css_selector('div[data-value="English language"]').click()
        sleep(2)
        driver.find_element_by_css_selector('div[data-is-receipt-checked] div[role="button"]').click()
        sleep(2)

        self.parse_2nd_page_review(driver)

    def parse_2nd_page_review(self, driver):
        driver.find_element_by_css_selector('input[aria-labelledby="i1"]').send_keys(choice(CITY_KG_EN))
        sleep(2)
        driver.find_element_by_css_selector('label[for="i9"]').click() # i9|12
        sleep(2)
        driver.find_element_by_css_selector('label[for="i22"]').click() # i22|25|28|31
        sleep(2)
        driver.find_element_by_css_selector('label[for="i38"]').click() # i38|41|44|47|50|53|56|59
        sleep(2)
        driver.find_element_by_css_selector('label[for="i69"]').click() # i66|69|72|75|78
        sleep(2)
        driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()
        
        self.parse_3th_page_review(driver)

    def parse_3th_page_review(self, driver):
        import ipdb; ipdb.set_trace()