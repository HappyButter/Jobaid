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