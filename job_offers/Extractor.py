import pymongo
import json
import environ

from django.http import JsonResponse

TECH_PATH = "../scrapers/info/technologies.json"
LANG_PATH = "../scrapers/info/languages.json"
ENV_PATH = "../jobaid/.env"

class Loader():

    def __init__(self, filename=""):
      self.loaded_set = []
      self.filename = filename

    def load_set(self):
        with open(self.filename, "r") as file:
            self.loaded_set = json.load(file)

    @staticmethod
    def env():
        envir = environ.Env(

        DEBUG=(bool, False)
        )
        # reading .env file
        environ.Env.read_env(env_file=ENV_PATH)

        MONGO_USER = envir('MONGO_USER')
        MONGO_PASS = envir('MONGO_PASS')
        MONGO_HOST = envir('MONGO_HOST')
        MONGO_NAME = envir('MONGO_NAME')
        MONGO_DATABASE_HOST = \
        'mongodb+srv://%s:%s@%s/%s' \
        % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_NAME)

        return MONGO_DATABASE_HOST

class DatabaseRecordsGetter():

    def __init__(self):
        self.client = pymongo.MongoClient(Loader.env())
        self.job_position = self.client.jobaid.job_position

    def records(self, records_type):
        records = []
        try:
            for record in self.job_position.find({}, {records_type: 1}):
                records.append(record)
        except ValueError:
            raise ValueError("Records not found")

        return records

    def count(self, seeken, records_type, threshold=0):
        records = self.records(records_type)
        if not records:
            return

        occurences = dict()
        counter = 0
        for item in seeken:
            for record in records:
                for element in record[records_type]:
                    if item.lower()  == element.lower():
                        counter += 1

            if counter >= threshold:
                occurences[item] = counter
            counter = 0

        return JsonResponse(dict(sorted(occurences.items(), key=lambda x: x[1], reverse=True)))


if __name__ == "__main__":
    pass

