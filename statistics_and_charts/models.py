from datetime import datetime
from mongoengine import fields, Document, EmbeddedDocument

class ChartsData(Document):

    company_size = fields.DictField(
        default={
            '<10' : 0,
            '10-50' : 0,
            '50-200' : 0,
            '200-500': 0,
            '500-1000': 0,
            '>1000': 0
        }
    )

    experience_level = fields.DictField(
        default={
            'junior' : 0,
            'mid' : 0,
            'senior' : 0
        }
    )

    languages = fields.DictField(
        default={
            'JavaScript': 0,
            'Python': 0,
            'Java': 0,
            'C#': 0,
            'PHP': 0,
            'C++': 0,
            'Others': 0
        }
    )

    technologies = fields.DictField(
        default={
            'Docker' : 0,
            'AWS' : 0,
            'Angular' : 0,
            'React' : 0,
            'Spring' : 0,
            'Kubernetes' : 0,
            '.NET' : 0,
            'Node.js' : 0,
            'MySQL' : 0
        }
    )

    contracts = fields.DictField(
        default={
            'b2b' : 0, 
            'uop' : 0
        }
    )

    date = fields.DateTimeField(defualt=datetime.utcnow)