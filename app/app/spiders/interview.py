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

CITY_KG_EN = ['Aidarken','Balykchy','Batken','Bishkek','Jalal-Abad','Kadamjai','Kaindy','Kant','Kara-Balta','Karakol',
              'Kara-Kul','Kara-Suu','Kemin','Kerben','Kok-Dzhangak','Kochkor-Ata','Kyzyl-Kiya','Mailuu-Suu','Naryn',
              'Nookat','Orlovka','Osh','Razzakov','Sulukta','Talas','Tash-Kumyr','Tokmok','Toktogul','Uzgen',
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
        sleep(5)

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
        sleep(5)

        self.click_by_label_for(5) # i5|8|11|14
        
        sleep(1)
        for idx in (2, 4, 6):
            table_1_query = ( 'div[aria-labelledby="i17"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        sleep(1)

        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_5th_page_review()


    def parse_5th_page_review(self):
        sleep(5)

        self.click_by_label_for(5) # i5|8|11|14
        
        sleep(1)
        self.click_by_label_for(21) # i21|24

        sleep(1)
        self.click_by_label_for(31) # i31|34

        sleep(1)
        self.click_by_label_for(41) # i41|44|47|50|53

        sleep(1)
        self.click_by_label_for(60) # i60|63|66|69|72

        sleep(1)
        self.click_by_label_for(79) # i79|82|85|88
        
        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_6th_page_review()

    def parse_6th_page_review(self):
        sleep(5)

        self.driver.find_element_by_css_selector('input[aria-labelledby="i1"]').send_keys(randrange(7))
        
        sleep(1)
        for idx in (2, 4, 6):
            table_1_query = ( 'div[aria-labelledby="i5"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        sleep(1)
        for idx in (2, 4, 6):
            table_1_query = ( 'div[aria-labelledby="i9"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        self.click_by_label_for(17) # i17|20

        sleep(1)
        for idx in (2, 4, 6, 8, 10, 12, 14):
            table_1_query = ( 'div[aria-labelledby="i26"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()


        sleep(1)
        for idx in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20):
            table_1_query = ( 'div[aria-labelledby="i30"] > div:nth-child(1) > '
                             f'div > div:nth-child({idx}) > span > div:nth-child({randrange(2, 6)}) > div > div' )

            table_1 = self.driver.find_element_by_css_selector(table_1_query).click()

        sleep(1)
        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

    def click_by_label_for(self, id):
        try:
            self.driver.find_element_by_css_selector(f'label[for="i{id}"]').click() # i9|12
        except:
            if self.debug == True:
                import ipdb; ipdb.set_trace()
            else:
                self.logger.critical(f"""Can't find label[for="i{id}"]""")

