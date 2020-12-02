import json
from hashlib import blake2b
from datetime import date

from scrapy import Spider
from scrapy.http import Request

class BulldogJobSpider(Spider):
    
    name = "bulldogjob"

    languages = ["Swift", "Assembler", "Pascal", "Elixir", "CSS3", "Scala", "HTML", "NoSQL", "Python", "Ruby", "C#", "Fortran", "Lisp", "Matlab","Objective-C", "HTML5", "Go", "SCSS", "Erlang", "PHP", "Kotlin", "SQL", "Rust", "Flutter", "Julia", "CSS", "C++", "Golang", "TypeScript", "JavaScript", "C", "Java", "VBA", "R", "Lua", "Dart"]

    languages_lower = ['swift', 'assembler', 'pascal', 'elixir', 'css3', 'scala', 'html', 'nosql', 'python', 'ruby', 'c#', 'fortran', 'lisp', 'matlab', 'objective-c', 'html5', 'go', 'scss', 'erlang', 'php', 'kotlin', 'sql', 'rust', 'flutter', 'julia', 'css', 'c++', 'golang', 'typescript', 'javascript', 'c', 'java', 'vba', 'r', 'lua', 'dart']

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
        # 'https://bulldogjob.pl/companies/jobs?page=10'
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
        # return set(item for item in technology_set if item.lower() in self.languages)
        # return set(self.languages[i] for item in technology_set if i = self.languages_lower.find(item.lower()) is not -1)
        lang_set = set()
        for item in technology_set:
            try:
                index = self.languages_lower.index(item.lower())
                lang_set.add(self.languages[index])
            except ValueError:
                continue

        return lang_set



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
            'b2b': 0,
            'uop': 0
        }

        for salary_div in ancestor.css('.salary'):
            contract_type = salary_div.css('.second-row::text').get().lower()

            per_hour = "hour" in contract_type or "godzina" in contract_type

            forks_str = salary_div.css('.money::text').get().replace(" ", "").lower()
            separator = forks_str.find("-")
            lower_boundary_keywords = ["from", "od"]
            upper_boundary_keywords = ["upto", "to", "do"]
            if separator != -1:
                if 'b2b' in contract_type:
                    salary['b2b'] = {
                        'min': int(forks_str[0:separator]) if not per_hour else int(forks_str[0:separator])*160,
                        'max': int(forks_str[separator + 1:]) if not per_hour else int(forks_str[separator + 1:])*160
                    }
                if 'umowa o pracę' in contract_type or 'employment contract' in contract_type:
                    salary['uop'] = {
                        'min': int(forks_str[0:separator]) if not per_hour else int(forks_str[0:separator])*160,
                        'max': int(forks_str[separator + 1:]) if not per_hour else int(forks_str[separator + 1:])*160
                    }
            else:
                forks_str = forks_str.replace("from", "").replace("od", "").replace("do", "").replace("upto", "").strip()
                if any([keyword in forks_str for keyword in lower_boundary_keywords]):
                    if 'b2b' in contract_type:
                        salary['b2b'] = {
                            'min': int(forks_str) if not per_hour else int(forks_str)*160
                        }
                    if 'umowa o pracę' in contract_type or 'employment contract' in contract_type:
                        salary['uop'] = {
                            'min': int(forks_str) if not per_hour else int(forks_str)*160
                        }
                elif any([keyword in forks_str for keyword in upper_boundary_keywords]):
                    if 'b2b' in contract_type:
                        salary['b2b'] = {
                            'max': int(forks_str) if not per_hour else int(forks_str)*160
                        }
                    if 'umowa o pracę' in contract_type or 'employment contract' in contract_type:
                        salary['uop'] = {
                            'max': int(forks_str) if not per_hour else int(forks_str)*160
                        }
        return salary


    def __generate_offer_hash(self, offer):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))

        return h.hexdigest()


    def parse_job_offer_page(self, response):
        sidebar_details = response.css('div.job-basic-details')
        main_content = response.css('div.job-content')
        
        offer = dict()

        offer['title'] = self.__get_position_title(main_content)
        offer['company'] = self.__get_company_name(main_content)
        offer['company_size'] = self.__get_company_size(sidebar_details)

        offer['location'] = {
            'address': self.__get_company_location(sidebar_details)
        }

        offer['expirience_level'] = self.__get_knowledge_level(main_content)

        skills_set = self.__get_languages_and_technologies_set(main_content)
        lang_set = self.__extract_languages(skills_set)

        offer['languages'] = list(lang_set)
        offer['technologies'] = list(skills_set - lang_set) # set differene

        offer['finances'] = {
            'contracts': self.__get_contract_types(sidebar_details),
            'salary': self.__get_salary_forks(sidebar_details)
        }

        offer['offer_hash'] = self.__generate_offer_hash(offer)

        offer_url = response.url
        offer['offer_link'] = offer_url
        offer['source_page'] = 'bulldogjob.pl'
        offer['date'] = date.today()
        offer['active'] = True

        yield offer


    def parse(self, response):
        for offer_list in response.css('ul.results-list'):
            links = [link.extract() for link in offer_list.css('a.job-item::attr(href)')]

            for link in links:
                yield Request(link, callback=self.parse_job_offer_page)

