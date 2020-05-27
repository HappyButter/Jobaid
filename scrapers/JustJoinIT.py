from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from forex_python.converter import CurrencyRates
from hashlib import blake2b
from time import sleep
from datetime import date

import json


class JustJoinIT:

    def __init__(self):
        c = CurrencyRates()
        self.languages = ["Swift", "Assembler", "Pascal", "Elixir", "CSS3", "Scala", "HTML", "NoSQL", "Python", "Ruby", "C#", "Fortran", "Lisp", "Matlab","Objective-C", "HTML5", "Go", "SCSS", "Erlang", "PHP", "Kotlin", "SQL", "Rust", "Flutter", "Julia", "CSS", "C++", "Golang", "TypeScript", "JavaScript", "C", "Java", "VBA", "R", "Lua", "Dart"]
        self.languages_lower = ['swift', 'assembler', 'pascal', 'elixir', 'css3', 'scala', 'html', 'nosql', 'python', 'ruby', 'c#', 'fortran', 'lisp', 'matlab', 'objective-c', 'html5', 'go', 'scss', 'erlang', 'php', 'kotlin', 'sql', 'rust', 'flutter', 'julia', 'css', 'c++', 'golang', 'typescript', 'javascript', 'c', 'java', 'vba', 'r', 'lua', 'dart']
        self.EUR = c.get_rate('EUR', 'PLN')
        self.USD = c.get_rate('USD', 'PLN')
        self.GBP = c.get_rate('GBP', 'PLN')
        print(" EUR:", self.EUR, " USD:", self.USD, " GBP:", self.GBP)
        self.links = []
        self.today = date.today()

        self.driver = webdriver.Firefox()
        self.driver.get("https://justjoin.it/")
        sleep(2)


    def get_links(self):
        
        SCROLL_PAUSE_TIME = 0.3
        iter = 1

        # save unique links
        main_window = self.driver.find_element_by_class_name('css-1macblb')
        old_offers = []
        while True:
            new_offers = self.driver.find_elements_by_class_name('css-18rtd1e')
            if old_offers == new_offers:
                return

            for offer in new_offers:
                link = offer.get_attribute('href')
                
                if link not in self.links:
                    self.links.append(link)
                else:
                    break
            
            # scroll offers
            arg = "arguments[0].scrollTo(0, document.documentElement.scrollHeight * {});".format(iter)
            self.driver.execute_script(arg , main_window)

            old_offers = new_offers
            sleep(SCROLL_PAUSE_TIME)
            iter+=1


    def source_page(self):
        return 'https://justjoin.it/'


    def get_title(self):
        return self.driver.find_element_by_class_name('css-1v15eia').text


    def get_company_name(self):
        return self.driver.find_element_by_class_name('css-l4opor').text


    def get_location(self):
        location = {
            'address' : self.driver.find_element_by_class_name('css-1d6wmgf').text
        }

        try:
            is_remote = self.driver.find_element_by_class_name('css-ei5nx6')
            if is_remote.text.lower() == 'remote':
                location['address'] = is_remote.text.lower()

        except NoSuchElementException:
            pass
        
        return location


    def get_company_size(self, company_info):
        info = company_info.text

        if "-" in info:
            x = info.replace("-", " ").split()
            return int(x[1])

        x = info\
            .replace(">", "")\
            .replace("+", "")\
            .replace("<", "")\
            .replace(" ", "")\
            .replace(",", "")
        
        if len(x) == 0:
            return None

        return int(x)


    def get_level(self, company_info):
        return company_info.text


    def get_contracts(self, contracts_info):
        contracts = {
            'b2b' : False,
            'uop' : False
        }

        if contracts_info.text == "b2b":
            contracts['b2b'] = True

        if contracts_info.text == "permanent":
            contracts['uop'] = True

        return contracts           


    def get_min_max_payment(self):
        salary_scraped_info = self.driver.find_element_by_class_name('css-8cywu8').text
        salary_scraped_info_splited = salary_scraped_info.split()

        if len(salary_scraped_info_splited) == 2:
            return None

        min = salary_scraped_info_splited[0] + salary_scraped_info_splited[1]
        min = int(min)

        if len(salary_scraped_info_splited) == 4:
            max = int(min)
            currency = salary_scraped_info_splited[2] 

        if len(salary_scraped_info_splited) == 7:
            max = salary_scraped_info_splited[3] + salary_scraped_info_splited[4]
            max = int(max)
            currency = salary_scraped_info_splited[5]

        min_max = {}
        if currency == 'PLN':        
            min_max['min'] = min
            min_max['max'] = max

        elif currency == 'EUR':        
            min_max['min'] = int(min * self.EUR)
            min_max['max'] = int(max * self.EUR)
        
        elif currency == 'USD':        
            min_max['min'] = int(min * self.USD)
            min_max['max'] = int(max * self.USD)   

        elif currency == 'GBP':        
            min_max['min'] = int(min * self.GBP)
            min_max['max'] = int(max * self.GBP)

        else: 
            return None

        return min_max


    def get_salary(self, contract_info):
        
        min_max = self.get_min_max_payment()

        salary = {
            'b2b' : None,
            'uop' : None
        } 

        if contract_info.text == "b2b":
            salary['b2b'] = min_max

        elif contract_info.text == "permanent":
            salary['uop'] = min_max

        return salary            


    def get_finances(self, contracts_info):
        contracts = self.get_contracts(contracts_info)
        salary = self.get_salary(contracts_info)

        finances = {}
        finances['contracts'] = contracts
        finances['salary'] = salary

        return finances


    def get_languages_and_technologies(self, tech_stack):
        languages = []
        technologies = []

        for skill in tech_stack:
            try:
                index = self.languages_lower.index(skill.text.lower())
                languages.append(self.languages[index])
            except:
                technologies.append(skill.text)
        
        return languages, technologies
    

    def generate_hash(self, offer):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))
        return h.hexdigest()


    def get_date(self):
        return self.today.strftime("%d-%m-%Y")


    def parse_to_dict(self, link):
        self.driver.get(link)
        sleep(1)
        
        company_size__contract_type__level = self.driver.find_elements_by_class_name('css-1ji7bvd')
        tech_stack = self.driver.find_elements_by_class_name('css-1eroaug')
        languages, technologies = self.get_languages_and_technologies(tech_stack)

        offer = {}

        offer['title'] = self.get_title()
        offer['company'] = self.get_company_name()
        offer['company_size'] = self.get_company_size(company_size__contract_type__level[0])
        offer['location'] = self.get_location()
        offer['experience_level'] = self.get_level(company_size__contract_type__level[2])
        offer['languages'] = list(languages)
        offer['technologies'] = list(technologies)
        offer['finances'] = self.get_finances(company_size__contract_type__level[1])
        offer['offer_hash'] = self.generate_hash(offer)
        offer['offer_link'] = link
        offer['source_page'] = self.source_page()
        offer['date'] = self.get_date()
        offer['active'] = True
        return offer


    def parse(self):
        self.get_links()

        progress_bar = len(self.links)
        print("Number of offers to scrap: " + str(progress_bar) )
        
        data = []
        for count, link in enumerate(self.links):
            try:
                offer = self.parse_to_dict(link)
                data.append(offer)
            except:
                pass

            if count % 20 == 0:
                percent = int(100*count/progress_bar)
                print("progress: ", str( percent ), " % ")

        with open('JustJoinIT.json', 'w', encoding='utf-8') as data_file:        
            json.dump(data, data_file, ensure_ascii=False, indent=4)   
        
        print("Done")

if __name__ == "__main__":
    a = JustJoinIT()
    a.parse()