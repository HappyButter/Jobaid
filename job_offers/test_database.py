import unittest
from django.test import SimpleTestCase
import sys
from .views import add_dict_to_database
from .models import JobPosition, Salary, Finances, Location
from mongoengine.queryset.visitor import Q

class TestDatabase(unittest.TestCase):
    def setUp(self):
        print("Clearing database.")
        offers = JobPosition.objects()
        for offer in offers:
            offer.delete()

    def test_data_base(self):
        sample_dict = {
            "title": "Remote Senior .Net Engineer",
            "company": "Sunscrapers Sp. z o.o.",
            "location": {
                "address": "Warsaw"
            },
            "company_size": 30,
            "experience_level": "senior",
            "languages": [
                "SQL",
                "C#"
            ],
            "technologies": [
                "SQL Server",
                "E-learning",
                "Microsoft",
                "English",
                ".NET",
                "Team player",
                "Security",
                "Proactivity",
                "React",
                "Polish",
                "Microsoft Server"
            ],
            "finances": {
                "contracts": {
                    "b2b": True,
                    "uop": False
                },
                "salary": {
                    "b2b": {
                        "min": 14000,
                        "max": 18000
                    },
                    "uop": None
                }
            },
            "offer_hash": "cbebdf008f894d163741d8ab131570172efd005800909ba5cda5d44b8197",
            "offer_link": "https://nofluffjobs.com/pl/job/remote-senior-net-engineer-sunscrapers-warsaw-emtjiuib",
            "source_page": "nofluffjobs.com",
            "date": "2020-06-06",
            "active": True
        }

        self.assertEqual("Added object to database.", add_dict_to_database(sample_dict))
        self.assertEqual("Object with same hash exists. Updated status.", add_dict_to_database(sample_dict))
        self.assertEqual("Object with same hash exists. Updated status.", add_dict_to_database(sample_dict))