import json
from hashlib import blake2b

from scrapy import Spider
from scrapy.http import Request

class BulldogJobSpider(Spider):
    name = "bulldogjob"

    # lowercase because some offers have languages starting with small letter...
    languages = ["java", "c#", "c", "c++", "python", "javascript", "typescript", "r", "php", "ruby on rails", "html5", "html", "css3", "scss", "css", "kotlin", "swift", "flutter", "sql", "scala", "rust", "go", "vba", "ruby", "objective-c", "nosql", "dart" "golang", "php 7"]

    start_urls = [
        'https://bulldogjob.pl/companies/jobs?page=1',
        'https://bulldogjob.pl/companies/jobs?page=2',
        'https://bulldogjob.pl/companies/jobs?page=3',
        'https://bulldogjob.pl/companies/jobs?page=4',
        'https://bulldogjob.pl/companies/jobs?page=5',
        'https://bulldogjob.pl/companies/jobs?page=6',
        'https://bulldogjob.pl/companies/jobs?page=7',
        'https://bulldogjob.pl/companies/jobs?page=8',
        'https://bulldogjob.pl/companies/jobs?page=9',
        'https://bulldogjob.pl/companies/jobs?page=10'
    ]


    def __get_position_title(self, ancestor):
        return ancestor.css('.data h1.desktop::text').get()


    def __get_company_name(self, ancestor):
        return ancestor.css('.data div.company-name::text').get().replace("\n", "").strip()


    def __get_knowledge_level(self, ancestor):
        return ancestor.css('.seniority strong::text').get().lower()    


    def __get_company_size(self, ancestor):
        try:
            company_size_div = ancestor.css('.sidebar-company .col-sm-9 .icons').extract()[0]
            start_idx = company_size_div.find("</svg>")
            # not sure if it is PEP8 compatible xD
            try:
                return int(
                    company_size_div[start_idx + 6:-6]
                        .replace(" ", "")
                        .replace("+", "")
                        .replace("&gt;", "")
                        .strip()
                )
            except ValueError:
                return None
        except IndexError:
            return None


    def __get_company_location(self, ancestor):
        try:
            location_div = ancestor.css('.flex.flex-end.details')[2]
            return location_div.css('span span::text').get().replace("\n", "")
        except IndexError:
            return None
    

    def __extract_languages(self, technology_set):
        return set(item for item in technology_set if item.lower() in self.languages)



    def __get_languages_and_technologies_set(self, ancestor):
        skill_set = set()

        for technology in ancestor.css('.technologies .technology span::text'):
            # split in case some creative HR put "HTML, CSS, JavaScript" instead of all items separated
            items = technology.get().split(",") 
            for item in items:
                item = item.strip()
                # excluding words specific for bulldogjob
                if item not in ["lub", "or", ""]:
                    skill_set.add(item)

        return skill_set


    def __get_contract_types(self, ancestor):
        contract = {
            'b2b': False,
            'uop': False
        }

        for contract_type in ancestor.css('.flex.flex-end.details span span::text'):
            contract_type = contract_type.get().lower().replace("\n", "")
            if contract_type == "b2b":
                contract['b2b'] = True
            if contract_type == 'umowa o pracę' or contract_type == 'employment contract':
                contract['uop'] = True
        
        return contract


    def __get_salary_forks(self, ancestor):
        salary = {
            'b2b': None,
            'uop': None
        }

        for salary_div in ancestor.css('.salary'):
            contract_type = salary_div.css('.second-row::text').get().lower()
            forks = salary_div.css('.money::text').get().replace(" ", "").lower()
            forks = forks.replace("from", "").replace("od", "").replace("do", "").replace("upto", "").replace("up", "").replace("to", "").strip()
            separator = forks.find("-")
            if 'b2b' in contract_type:
                salary['b2b'] = {
                    'min': int(forks[0:separator]),
                    'max': int(forks[separator + 1:])
                }
            if 'umowa o pracę' in contract_type or 'employment contract' in contract_type:
                salary['uop'] = {
                    'min': int(forks[0:separator]),
                    'max': int(forks[separator + 1:])
                }

        return salary


    def __generate_offer_hash(self, offer, internal_id):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))
        h.update(internal_id.encode('utf-8'))

        return h.hexdigest()


    def parse_job_offer_page(self, response):
        sidebar_details = response.css('div.job-basic-details')
        main_content = response.css('div.job-content')
        
        offer = dict()

        offer['title'] = self.__get_position_title(main_content)
        offer['company'] = self.__get_company_name(main_content)
        offer['level'] = self.__get_knowledge_level(main_content)

        skills_set = self.__get_languages_and_technologies_set(main_content)
        lang_set = self.__extract_languages(skills_set)

        offer['languages'] = list(lang_set)
        offer['technologies'] = list(skills_set - lang_set) # set differene


        offer['company_size'] = self.__get_company_size(sidebar_details)
        offer['location'] = self.__get_company_location(sidebar_details)

        offer['finances'] = {
            'contract': self.__get_contract_types(sidebar_details),
            'salary': self.__get_salary_forks(sidebar_details)
        }

        offer_url = response.url
        offer['offer_link'] = offer_url
        offer['source_page'] = offer_url[8:offer_url.find('/companies')] # yes yes yes, I know it's greeeeeedy

        id_start = offer_url.find('jobs/')
        id_end= offer_url.find('-')
        internal_offer_id = offer_url[id_start:id_end]

        offer['hash'] = self.__generate_offer_hash(offer, internal_offer_id)

        yield offer


    def parse(self, response):
        for offer_list in response.css('ul.results-list'):
            links = [link.extract() for link in offer_list.css('a.job-item::attr(href)')]

            for link in links:
                yield Request(link, callback=self.parse_job_offer_page)

