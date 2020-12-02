# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from hashlib import blake2b
from datetime import date


class TeamquestSpider(scrapy.Spider):
    name = 'TeamQuest'

    start_urls = [
        'https://teamquest.pl/praca-w-it/s/' +
        str(number) for number in range(1, 10)]

    url_prefix = 'https://teamquest.pl'
    languages = [
        "java",
        "c#",
        "c",
        "c++",
        "python",
        "javascript",
        "typescript",
        "r",
        "php",
        "ruby on rails",
        "html5",
        "html",
        "css3",
        "scss",
        "css",
        "kotlin",
        "swift",
        "flutter",
        "sql",
        "scala",
        "rust",
        "go",
        "vba",
        "ruby",
        "objective-c",
        "nosql",
        "dart"
        "golang",
        "php 7"]

    def _get_position_title(self, ancestor):
        return ancestor.css('h1::text').get()

    def _get_company_location(self, ancestor):
        try:
            returned = [location for location in ancestor.css(
                '.job-location-btn .strong::text').extract() if location.strip() != ''][0].strip()
            if returned == 'Praca zdalna':
                returned = 'remote'
            return returned
        except IndexError:
            return None

    def _extract_languages(self, technology_set):
        try:
            return set(item for item in technology_set if item.lower()
                       in TeamquestSpider.languages)
        except IndexError:
            return None

    def _get_languages_and_technologies_set(self, ancestor):
        try:
            return set(technology for technology in ancestor.css(
                '.tag-xs::text').extract())
        except IndexError:
            return None

    def _get_contract_types(self, ancestor):
        contract = {
            'b2b': False,
            'uop': False
        }

        for contract_type in ancestor.css('.details .label-blue::text'):
            contract_type = contract_type.get().lower().replace("\n", "")
            if contract_type == "b2b / kontrakt" or contract_type == 'umowa zlecenie' or contract_type == 'umowa o dzieło' or contract_type == "dowolna":
                contract['b2b'] = True
            if contract_type == 'umowa o pracę' or contract_type == "dowolna":
                contract['uop'] = True

        return contract

    def _get_salary_forks(self, ancestor):
        salary = {
            'b2b': None,
            'uop': None
        }

        contract_type = self._get_contract_types(ancestor)
        forks = ancestor.css('.job-sallary::text').extract()
        forks = [
            actual_forks for actual_forks in forks if actual_forks.strip() != '']

        if not forks:
            return salary

        forks = forks[0].replace('PLN', '').strip()
        separator = forks.find("-")
        if contract_type['b2b']:
            salary['b2b'] = {
                'min': int(forks[0:separator]),
                'max': int(forks[separator + 1:])
            }
        if contract_type['uop']:
            salary['uop'] = {
                'min': int(forks[0:separator]),
                'max': int(forks[separator + 1:])
            }

        return salary

    def _generate_offer_hash(self, offer):
        string = json.dumps(offer, sort_keys=True)
        h = blake2b(digest_size=30)
        h.update(string.encode('utf-8'))

        return h.hexdigest()

    def parse_job_offer_page(self, response):

        offer = dict()

        offer['title'] = self._get_position_title(response)
        offer['company'] = None
        offer['company_size'] = None
        offer['location'] = {
            'address': self._get_company_location(response)
        }
        offer['experience_level'] = None

        skills_set = self._get_languages_and_technologies_set(response)
        lang_set = self._extract_languages(skills_set)

        offer['languages'] = list(lang_set)
        offer['technologies'] = list(skills_set - lang_set)
        offer['finances'] = {
            'contracts': self._get_contract_types(response),
            'salary': self._get_salary_forks(response)
        }

        offer['offer_hash'] = self._generate_offer_hash(offer)

        offer_url = response.url
        offer['offer_link'] = offer_url
        offer['source_page'] = ''.join(
            TeamquestSpider.url_prefix.split('https://'))  # get rid of https://

        offer['date'] = date.today()
        offer['active'] = True

        yield offer

    def parse(self, response):

        job_offers = response.css('h4 > a')
        links = job_offers.css('::attr(href)').extract()
        links = [TeamquestSpider.url_prefix + link for link in links]

        for link in links:
            yield Request(link, callback=self.parse_job_offer_page)
