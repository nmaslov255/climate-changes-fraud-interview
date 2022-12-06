import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

from time import sleep
from datetime import datetime as dt
from random import choice, randrange

import traceback

START_URL = 'https://forms.gle/s8ME2PMP9o5PMKsW7'

CITY_KG_RU = ['Айдаркен','Балыкчы','Баткен','Бишкек','Джалал-Абад','Кадамжай','Каинды','Кант','Кара-Балта','Каракол',
              'Кара-Куль','Кара-Суу','Кемин','Кербен','Кок-Джангак','Кочкор-Ата','Кызыл-Кия','Майлуу-Суу','Нарын',
              'Ноокат','Орловка','Ош','Раззаков','Сулюкта','Талас','Таш-Кумыр','Токмок','Токтогул','Узген',
              'Чолпон-Ата','Шопоков']

CITY_KG_EN = ['Aidarken','Balykchy','Batken','Bishkek','Jalal-Abad','Kadamjai','Kaindy','Kant','Kara-Balta','Karakol',
              'Kara-Kul','Kara-Suu','Kemin','Kerben','Kok-Dzhangak','Kochkor-Ata','Kyzyl-Kiya','Mailuu-Suu','Naryn',
              'Nookat','Orlovka','Osh','Razzakov','Sulukta','Talas','Tash-Kumyr','Tokmok','Toktogul','Uzgen',
              'Cholpon-Ata','Shopokov']

now = dt.now()

def generate_with_probability(elements, distribution):
    if sum(distribution) != 1:
        raise Exception('Probability must me equal 1 (100%)')

    sample = []
    for element, percent in zip(elements, distribution):
        sample += [element] * int(percent*100)
    return sample

def choice_with_probability(elements, distribution):
    return choice(generate_with_probability(elements, distribution))


class InterviewSpider(scrapy.Spider):
    name = 'interview'
    allowed_domains = [START_URL]
    start_urls = [START_URL]

    debug = True
    driver = None
    answers = [f"Date: {now.year}/{now.month}/{now.day} {now.hour}:{now.minute}"]

    def start_requests(self):
        yield SeleniumRequest(url=START_URL, callback=self.parse_1st_page_review)

    def parse_1st_page_review(self, responce):
        self.driver = responce.meta['driver']

        sleep(2)
        self._click_by_label_for(
            choice_with_probability([5, 8, 11], [0.1, 0.25, 0.65]), 
            'Choose language', 
            {5: 'English language', 8: 'Русский язык', 11: 'Кыргыз тили'}
        ) # i5|8|11
        sleep(2)
        self.driver.find_element_by_css_selector('div[data-is-receipt-checked] div[role="button"]').click()

        self.parse_2nd_page_review()

    def parse_2nd_page_review(self):
        sleep(5)

        self._input_form_for(1, 'Please indicate your city', choice(CITY_KG_EN))
        sleep(2)

        self._click_by_label_for(9, 'Please indicate your gende', {9: 'Female', 12: 'Male'}) # i9|12
        sleep(2)
        self._click_by_label_for(22, 'Please indicate your age', 
            {22: '16-24', 25: '25-44', 28: '45-64', 31: 'Prefer not to say'}
        ) # i22|25|28|31
        sleep(2)

        self._click_by_label_for(38, 'Please indicate your household income per month',
            {38: '10,000 KGS', 41: '20,000 KGS', 44: '30,000 KGS', 47: '40,000 KGS', 50: '50,000 KGS', 
             53: '75,000 KGS and more', 56: 'I don\'t know', 59: 'Prefer not to say'}
         ) # i38|41|44|47|50|53|56|59
        sleep(2)
        self._click_by_label_for(69, 'Please indicate your education level', {
            66: 'No Formal Education', 69: 'Primary Education', 72: 'Secondary', 75: 'University Degree', 
            78: 'Master or equivalent'}
        ) # i66|69|72|75|78
        sleep(2)
        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()
        
        self.parse_3th_page_review()

    def parse_3th_page_review(self):
        sleep(5)
        self._click_by_label_for(5,
            'Do any of your friends, family or colleagues make sacrifices to protect the environment?',
            {5: 'Never', 8: 'Very rarely', 11: 'Rarely', 14: 'Sometimes', 17: 'Always', 20: 
            'I dont know we never discuss this'}
        ) # i5|8|11|14|17|20

        self._input_table_form_for(
            23, 
            ('How much influence do your family, friends and colleagues have on your decision to make sacrifices '
             'to protect the environment?'), 
            ['Family', 'Friends', 'Colleagues'], 
            [randrange(5) for _ in range(3)],
            ['Never', 'Rarely', 'From time to time', 'Often', 'Always']
        )
        sleep(1)
        self._input_table_form_for(
            27, 
            ('What do you think people would think of you if you made sacrifices to protect '
             'the environment?'), 
            ['Family', 'Friends', 'Colleagues'], 
            [randrange(5) for _ in range(3)],
            ['Very Unfavourable: They try to stop me', 'Unfavourable but do not try to stop me',
             'They don\'t care', 'Favorable: They support me but wont make sacrifices themselves', 
             'Very favorable: They d like to also make sacrifices']
        )
        sleep(1)

        self._click_by_label_for(35, 
            ('Following environmental influencers: I follow influencers on social media (e.g. YouTube, Instagram) '
            'who post about the environment and sustainability'),
            {35: 'I never do, I am not interested', 38: 'I rarely do', 
             41: 'From time to time', 44: 'Very often'}
        ) # i35|38|41|44

        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_4th_page_review()

    def parse_4th_page_review(self):
        sleep(5)

        self._click_by_label_for(5, 'How easy would you find it to make sacrifices to protect the environment?',
            {5: 'Very Difficult', 8: 'Difficult', 11: 'Easy', 14: 'Very Easy'}
        ) # i5|8|11|14
        
        sleep(1)
        self._input_table_form_for(
            17, 
            ('I feel I could influence my workplace/boss to be more environmentally '
             'friendly (pollute less, use electric car, use less plastic…)'), 
            ['Workplace / Colleagues / Boss', 'Friends', 'Colleagues'], 
            [randrange(5) for _ in range(3)],
            ['I could NOT influence them at all', 'It is not likely I could influence them',
             'Maybe / not sure', 'I could likely influence them', 'I could very likely influence them']
        )
        sleep(1)

        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_5th_page_review()


    def parse_5th_page_review(self):
        sleep(5)

        self._click_by_label_for(5, 'I believe that Air quality in my city is',
            {5: 'Very bad', 8: 'Bad', 11: 'Good', 14: 'Very good'}
        ) # i5|8|11|14
        
        sleep(1)
        self._click_by_label_for(21, 'I know what PM2.5 means', 
            {21: 'Yes', 24: 'No'}
        ) # i21|24

        sleep(1)
        self._click_by_label_for(31, 'I understand the danger of air pollution',
            {31: 'Yes', 34: 'No'}
        ) # i31|34

        sleep(1)
        self._click_by_label_for(41, 'How important is the issue of climate change to you personally?', 
            {41: 'This is not an issue at all', 44: 'I don\'t care about this issue', 47: 'I am indifferent', 
             50: 'I somewhat care', 53: 'I very much care'}
        ) # i41|44|47|50|53

        sleep(1)
        self._click_by_label_for(60, 'How much do you know about climate change', 
            {60: 'This is not an issue', 63: 'I don\'t know anything', 66: 'I am not interested to know', 
             69: 'I know a little bit', 72: 'I know a lot'}
        ) # i60|63|66|69|72

        sleep(1)
        self._click_by_label_for(79, 'Climate change does not exist', 
            {79: 'Climate change is caused only by natural processes', 
             82: 'Climate change is caused only by human activity', 85: 'I don’t know what is causing climate change',
             88: 'Climate change does not exist'}
        ) # i79|82|85|88
        
        self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        self.parse_6th_page_review()

    def parse_6th_page_review(self):        
        sleep(5)

        self._input_form_for(1, 'Average smoking member in your family', randrange(5))
        sleep(1)
        self._input_table_form_for(
            5, 
            ('What do you use for home heating'),
            ['Coal', 'Gas', 'Electricity'], 
            [randrange(4) for _ in range(3)],
            ['Never', 'Rarely', 'From time to time', 'Always']
        )

        sleep(1)
        self._input_table_form_for(
            9, 
            ('What do you use for cooking meal'),
            ['Coal', 'Gas', 'Electricity'], 
            [randrange(4) for _ in range(3)],
            ['Never', 'Rarely', 'From time to time', 'Always']
        )

        self._click_by_label_for(17, 'Do you use an air purifier at home', {17: 'Yes', 20: 'No'}) # i17|20

        sleep(1)
        self._input_table_form_for(
            26, 
            ('Have you experienced the following in the last three months?'),
            ['Cough', 'Dry Throat', 'Sneezing/allergy', 'Flu', 'Asthma', 'Fever', 'Other'], 
            [randrange(5) for _ in range(7)],
            ['Never', 'Very Rarely', 'Often', 'Nearly Always', 'Always']
        )

        sleep(1)

        self._input_table_form_for(
            30, 
            ('Pro-Environmental Behaviour / Intentions'),
            ['I leave the water running while I brush my teeth', 
             'I forget to turn off the light when I leave my room', 
             'I leave the fridge door open while I think about what I go eat', 
             'Outside I put my trash in the bin',
             'I leave the TV on while I\'m doing other things in the house', 
             'I read documents or books about environmental protection', 
             'I am willing to change my behaviour to change the state of the environment',
             'I would support those who care about the environment',
             'I believe that more trees should be planted',
             'I try to push my company/work to be more green'], 
            [randrange(5) for _ in range(10)],
            ['Never', 'Very rarely', 'Sometime', 'Often', 'Always']
        )

        sleep(1)
        # self.driver.find_elements_by_css_selector('div[data-is-receipt-checked] div[role="button"]')[1].click()

        import ipdb; ipdb.set_trace()

    def _input_table_form_for(self, id, title, questions, answer_options, answer_text):
        answer = f"{title}\n\n"
        try:
            for idx, question in enumerate(questions):
                answer_id = (idx+1)*2
                table_query = (f'div[aria-labelledby="i{id}"] > div:nth-child(1) > div > '
                               f'div:nth-child({answer_id}) > span > div:nth-child({answer_options[idx]+2}) > '
                                'div > div')

                self.driver.find_element_by_css_selector(table_query).click()
                answer += f'{question}: {answer_text[answer_options[idx]]}\n'

            self.answers.append(answer)
        except:
            if self.debug == True:
                import ipdb; ipdb.set_trace()
            else:
                self.logger.critical(f"""Can't find input[aria-labelledby="i{id}"]""")        
            traceback.print_exc()

    def _input_form_for(self, id, question, answer):
        try:
            self.driver.find_element_by_css_selector(f'input[aria-labelledby="i{id}"]').send_keys(answer)
            self.answers.append(f"{question}: {answer}")
        except:
            if self.debug == True:
                import ipdb; ipdb.set_trace()
            else:
                self.logger.critical(f"""Can't find input[aria-labelledby="i{id}"]""")        
            traceback.print_exc()

    def _click_by_label_for(self, id, question, answers):
        try:
            self.driver.find_element_by_css_selector(f'label[for="i{id}"]').click()
            self.answers.append(f"{question}: {answers[id]}")
        except:
            if self.debug == True:
                import ipdb; ipdb.set_trace()
            else:
                self.logger.critical(f"""Can't find label[for="i{id}"]""")
        traceback.print_exc()


