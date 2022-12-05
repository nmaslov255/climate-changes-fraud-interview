import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

from time import sleep
from random import choice, randrange

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

    debug = True
    driver = None

    def start_requests(self):
        yield SeleniumRequest(url=START_URL, callback=self.parse_1st_page_review)

    def parse_1st_page_review(self, responce):
        self.driver = responce.meta['driver']

        sleep(5)
        self.driver.find_element_by_css_selector('div[data-value="English language"]').click()
        sleep(2)
        self.driver.find_element_by_css_selector('div[data-is-receipt-checked] div[role="button"]').click()
        sleep(2)

        self.parse_2nd_page_review()

    def parse_2nd_page_review(self):

        self.driver.find_element_by_css_selector('input[aria-labelledby="i1"]').send_keys(choice(CITY_KG_EN))
        sleep(2)
        self.click_by_label_for(9) # i9|12
        sleep(2)
        self.click_by_label_for(22) # i22|25|28|31
        sleep(2)
        self.click_by_label_for(38) # i38|41|44|47|50|53|56|59
        sleep(2)
        self.click_by_label_for(69) # i66|69|72|75|78
        sleep(2)
        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()
        
        self.parse_3th_page_review()

    def parse_3th_page_review(self):
        sleep(5)
        self.click_by_label_for(5) # i5|8|11|14|17|20
        import ipdb; ipdb.set_trace()

        for idx in (2, 4, 6):
            table_1_query = ( 'div[aria-labelledby="i23"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        sleep(1)

        for idx in (2, 4, 6):
            table_1_query = ( 'div[aria-labelledby="i27"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        sleep(1)
        self.click_by_label_for(35) # i35|38|41|44

        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_4th_page_review()

    def parse_4th_page_review(self):
        import ipdb; ipdb.set_trace()
        pass

    def click_by_label_for(self, id):
        try:
            self.driver.find_element_by_css_selector(f'label[for="i{id}"]').click() # i9|12
        except:
            if self.debug == True:
                import ipdb; ipdb.set_trace()
            else:
                self.logger.critical(f"""Can't find label[for="i{id}"]""")

