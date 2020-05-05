from mongoengine import fields, Document, EmbeddedDocument

class Salary(EmbeddedDocument):
    b2b = fields.DictField(default={'min': 0, 'max': 50000})
    uop = fields.DictField(default={'min': 0, 'max': 50000})

class Finances(EmbeddedDocument):
    contracts = fields.DictField(default={'b2b': False, 'uop': False})
    salary = fields.EmbeddedDocumentField(Salary)

class JobOffer(Document):
    title = fields.StringField(max_length=100)
    company = fields.StringField(max_length=100)
    location = fields.StringField(max_length=100)
    companiy_size = fields.IntField(min_value = 0)
    expirience_level = fields.StringField(max_length=100)
    languages = fields.ListField(fields.StringField(max_length=20))
    technologies = fields.ListField(fields.StringField(max_length=40))
    finances = fields.EmbeddedDocumentField(Finances)
    offer_link = fields.StringField(max_length=100)
    source_page = fields.URLField(max_length=100)
    offer_hash = fields.StringField(max_length=32)

    def __str__(self):
        return self.title