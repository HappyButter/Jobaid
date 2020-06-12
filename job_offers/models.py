from mongoengine import fields
from common.models import JobPosition


class JobOffer(JobPosition):
    title = fields.StringField()
    company = fields.StringField(max_length=100)
    languages = fields.ListField(fields.StringField())
    offer_link = fields.URLField()
    source_page = fields.StringField(max_length=100)
    active = fields.BooleanField(default=True)
    offer_hash = fields.StringField(max_length=62)

    def __str__(self):
        return f'Title: {self.title}' + f'\nCompany: {self.company}' + f'\nCompany Size: {self.company_size}' + f'\nAddress: {self.location.address}' + f'\nExperience Level: {self.experience_level}' + f'\nCompany Size: {self.company_size}' + f'\nTechnologies: {self.technologies}' + f'\nLanguages: {self.languages}' + f'\nContracts: {self.finances.contracts}' + f'\nSalary b2b: {self.finances.salary.b2b}' + f'\nSalary uop: {self.finances.salary.uop}' + f'\nDate: {self.date}' + f'\nSource Page: {self.source_page}' + f'\nIs Active: {self.active}' + f'\nOffer hash: {self.offer_hash}'