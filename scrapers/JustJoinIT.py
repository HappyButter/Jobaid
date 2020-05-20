from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from hashlib import blake2b
from time import sleep
import json


class JustJoinIT:

    def __init__(self):
        self.languages = ["java", "c#", "c", "c++", "python", "javascript", "typescript", "r", "php", "ruby", "html5", "html", "css3", "scss", "css", "kotlin", "swift", "flutter", "sql", "scala", "rust", "go", "vba", "ruby", "objective-c", "nosql", "dart", "golang", "matlab"]
        self.EUR = 4.54
        self.USD = 4.20
        self.GBP = 5.20
        self.links = []

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


    def get_contract(self, contract_info):
        contract = {
            'b2b' : False,
            'uop' : False
        }

        if contract_info.text == "b2b":
            contract['b2b'] = True

        if contract_info.text == "permanent":
            contract['uop'] = True

        return contract            


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


    def get_finances(self, contract_info):
        contract = self.get_contract(contract_info)
        salary = self.get_salary(contract_info)

        finances = {}
        finances['contract'] = contract
        finances['salary'] = salary

        return finances


    def get_languages_and_technologies(self, tech_stack):
        languages = []
        technologies = []

        for skill in tech_stack:
            if skill.text.lower() in self.languages:
                languages.append(skill.text.lower())
            else:
                technologies.append(skill.text.lower())
        
        return languages, technologies
    

    def generate_hash(self, offer):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))
        return h.hexdigest()


    def parse_to_dict(self, link):
        self.driver.get(link)
        sleep(1)
        
        company_size__contract_type__level = self.driver.find_elements_by_class_name('css-1ji7bvd')
        tech_stack = self.driver.find_elements_by_class_name('css-1eroaug')
        
        offer = {}

        offer['title'] = self.get_title()
        offer['company'] = self.get_company_name()
        offer['company_size'] = self.get_company_size(company_size__contract_type__level[0])
        offer['location'] = self.get_location()
        offer['expirience_level'] = self.get_level(company_size__contract_type__level[2])
        
        languages, technologies = self.get_languages_and_technologies(tech_stack)
        offer['languages'] = list(languages)
        offer['technologies'] = list(technologies)
        offer['finances'] = self.get_finances(company_size__contract_type__level[1])
        offer['hash'] = self.generate_hash(offer)

        offer['source_page'] = self.source_page()
        offer['link'] = link

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
                print("progress: " + str( int((iter/progress_bar) * 100) ) + "%")

        with open('JustJoinIT.json', 'w', encoding='utf-8') as data_file:        
            json.dump(data, data_file, ensure_ascii=False, indent=4)   
        
        print("Done")