from mongoengine import fields, Document, EmbeddedDocument

class Salary(EmbeddedDocument):
    b2b = fields.DictField(default={'min': 0, 'max': 0})
    uop = fields.DictField(default={'min': 0, 'max': 0})

class Finances(EmbeddedDocument):
    contracts = fields.DictField(default={'b2b': False, 'uop': False})
    salary = fields.EmbeddedDocumentField(Salary)

class Location(EmbeddedDocument):
    adress = fields.StringField(max_length=50)
    coordinates = fields.GeoPointField()
    

class JobPosition(Document):
    title = fields.StringField(max_length=100)
    location = fields.EmbeddedDocumentField(Location)
    
    company = fields.StringField(max_length=100)
    companiy_size = fields.IntField(min_value = 0)

    expirience_level = fields.StringField(max_length=100)
    languages = fields.ListField(fields.StringField(max_length=20))
    technologies = fields.ListField(fields.StringField(max_length=40))

    finances = fields.EmbeddedDocumentField(Finances)

    active = fields.BooleanField(default=True)
    offer_hash = fields.StringField(max_length=32)

    meta = {'allow_inheritance': True}

    def __str__(self):
        return self.title

class JobOffer(JobPosition):
    offer_link = fields.URLField()
    source_page = fields.StringField(max_length=100)

