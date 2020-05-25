from scrapy import Spider
from scrapy.http import Request
from hashlib import blake2b
from datetime import date
import json

class NoFluffJobsSpider(Spider):
    name = "nofluffjobs"

    languages = ["Swift", "Assembler", "Pascal", "Elixir", "CSS3", "Scala", "HTML", "NoSQL", "Python", "Ruby", "C#", "Fortran", "Lisp", "Matlab","Objective-C", "HTML5", "Go", "SCSS", "Erlang", "PHP", "Kotlin", "SQL", "Rust", "Flutter", "Julia", "CSS", "C++", "Golang", "TypeScript", "JavaScript", "C", "Java", "VBA", "R", "Lua", "Dart"]

    languages_lower = ['swift', 'assembler', 'pascal', 'elixir', 'css3', 'scala', 'html', 'nosql', 'python', 'ruby', 'c#', 'fortran', 'lisp', 'matlab', 'objective-c', 'html5', 'go', 'scss', 'erlang', 'php', 'kotlin', 'sql', 'rust', 'flutter', 'julia', 'css', 'c++', 'golang', 'typescript', 'javascript', 'c', 'java', 'vba', 'r', 'lua', 'dart']


    start_urls = [
        'https://nofluffjobs.com/pl/jobs/remote?criteria=city%3Dremote,warszawa,wroclaw,krakow,gdansk,poznan,trojmiasto,slask,lodz,katowice,lublin,szczecin,bydgoszcz,bialystok,gdynia,gliwice,sopot'
        ]


    def __get_position_title(self, ancestor):
        title = ancestor.css('.posting-details-description h1::text').get()
        if title == None:
            return None
        return title.strip()


    def __get_company_name(self, ancestor):
        name = ancestor.css('.company-name::text').get()
        if name == None:
            name = ancestor.css('.d-block:nth-child(2) .d-flex .mb-0::text').get()
            if name == None:
                return None
            return name.strip()
        return name.strip()


    def __get_location(self, ancestor):
        location = ancestor.css('.text-break::text').get()
        if location == None:
            location = ancestor.css('.remote::text').get()
            if location == None:
                return None
            return location.strip()
        return location.strip()


    def __get_company_size(self, ancestor):
        size = ancestor.css('.d-block:nth-child(3) .d-flex .mb-0::text').get()
        if size == None:
            return None
        if '-' in size:
            tmp = size.split('-')
            return int(tmp[1])
        return int(size.replace('+', ''))


    def __get_experience_level(self, ancestor):
        experience = ancestor.css('.active p::text').getall()
        if experience == None:
            return None
        if "Junior" in experience or "Stażysta" in experience:
            return "junior"
        if "Mid" in experience:
            return "mid"
        if "Senior" in experience or "Expert" in experience:
            return "senior"


    def __get_languages_and_technologies_set(self, ancestor):
        skill_set = set()
        all_set = ancestor.css('.btn-outline-success::text').getall()
        if all_set != None:
            for item in all_set:
                item = item.strip()
                skill_set.add(item)
        return skill_set


    def __extract_languages(self, technology_set):
        skill_set = set()
        for item in technology_set:
            try:
                index = self.languages_lower.index(item.lower())
                skill_set.add(self.languages[index])
            except ValueError:
                continue
        return skill_set


    def __get_finances(self, ancestor):
        finances = {
            'contracts' : {
                'b2b': False,
                'uop': False
            },
            'salary' : {
                'b2b': None,
                'uop': None
            }
        }
        contracts = list(zip(ancestor.css('.salary .type::text').getall(), ancestor.css('.salary .mb-0::text').getall()))
        for contract in contracts:
            if contract[0].strip() == '+ vat (B2B) miesięcznie':
                finances['contracts']['b2b'] = True
                forks = contract[1].replace(' ', '').replace("PLN", "")
                separator = forks.find("-")
                finances['salary']['b2b'] = {
                    'min': int(forks[0:separator]),
                    'max': int(forks[separator + 1:])
                }
            if contract[0].strip() == '+ vat (B2B) godzinowo':
                finances['contracts']['b2b'] = True
                forks = contract[1].replace(' ', '').replace("PLN", "")
                separator = forks.find("-")
                finances['salary']['b2b'] = {
                    'min': 168 * int(forks[0:separator]),
                    'max': 168 * int(forks[separator + 1:])
                }
            if contract[0].strip() == '+ vat (B2B) dziennie':
                finances['contracts']['b2b'] = True
                forks = contract[1].replace(' ', '').replace("PLN", "")
                separator = forks.find("-")
                finances['salary']['b2b'] = {
                    'min': 21 * int(forks[0:separator]),
                    'max': 21 * int(forks[separator + 1:])
                }
            if contract[0].strip() == 'brutto (umowa o pracę) miesięcznie':
                finances['contracts']['uop'] = True
                forks = contract[1].replace(' ', '').replace("PLN", "")
                separator = forks.find("-")
                finances['salary']['uop'] = {
                    'min': int(forks[0:separator]),
                    'max': int(forks[separator + 1:])
                }
        return finances


    def __generate_offer_hash(self, offer):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))
        return h.hexdigest()


    def parse_offer(self, ancestor):
        offer = dict()
        offer['title'] = self.__get_position_title(ancestor)
        offer['company'] = self.__get_company_name(ancestor)
        offer['location'] = { 'address': self.__get_location(ancestor)}
        offer['company_size'] = self.__get_company_size(ancestor)
        offer['experience_level'] = self.__get_experience_level(ancestor)
        skills_set = self.__get_languages_and_technologies_set(ancestor)
        lang_set = self.__extract_languages(skills_set)
        offer['languages'] = list(lang_set)
        offer['technologies'] = list(skills_set - lang_set)
        finances = self.__get_finances(ancestor)
        offer['finances'] = {
            'contracts' : finances['contracts'],
            'salary' : finances['salary']
        }
        offer['offer_hash'] = self.__generate_offer_hash(offer)
        offer_url = ancestor.url
        offer['offer_link'] = offer_url
        offer['source_page'] = offer_url[8:offer_url.find('/pl/job')]
        offer['date'] = date.today()
        offer['active'] = True
        yield offer


    def parse_page(self, response):
        links = response.css('.posting-list-item::attr(href)').getall()
        source = 'https://nofluffjobs.com'
        for link in links:
            yield Request(source + link, callback=self.parse_offer)


    def parse(self, response):
        number = int(response.css('.page-item~ .disabled+ .page-item .page-link::text').get())
        source = 'https://nofluffjobs.com/pl/jobs/remote?criteria=city%3Dremote,warszawa,wroclaw,krakow,gdansk,poznan,trojmiasto,slask,lodz,katowice,lublin,szczecin,bydgoszcz,bialystok,gdynia,gliwice,sopot&page='
        for i in range(number):
            yield Request(source + str(i+1), callback=self.parse_page)
