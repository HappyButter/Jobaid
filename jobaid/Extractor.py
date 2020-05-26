from django.http import JsonResponse
import pymongo
import json
import environ


class Loader():

    def __init__(self, filename=""):
      self.loaded_set = []
      self.filename = filename

    def load_set(self):
        with open(self.filename, "r") as file:
            self.loaded_set = json.load(file)

    @property
    def env(self):
        envi = environ.Env(

        DEBUG=(bool, False)
        )
        # reading .env file
        environ.Env.read_env()

        MONGO_USER = envi('MONGO_USER')
        MONGO_PASS = envi('MONGO_PASS')
        MONGO_HOST = envi('MONGO_HOST')
        MONGO_NAME = envi('MONGO_NAME')
        MONGO_DATABASE_HOST = \
        'mongodb+srv://%s:%s@%s/%s' \
        % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_NAME)

        return MONGO_DATABASE_HOST

class DatabaseRecordsGetter():

    def __init__(self):
        self.client = pymongo.MongoClient(Loader().env)
        self.job_position = self.client.jobaid.job_position

    def records(self, records_type):
        records = []
        try:
            for record in self.job_position.find({}, {records_type: 1}):
                records.append(record)
        except ValueError:
            raise ValueError("Records not found")

        return records

    def count(self, seeken, records_type, save=False):
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

            occurences[item] = counter
            counter = 0

        sorted_occurences = dict(sorted(occurences.items(), key=lambda x: x[1], reverse=True))

        if save:
            with open(records_type + "_occurences.json", "w", encoding="utf-8") as f:
                json.dump(sorted_occurences, f, ensure_ascii=False, indent=4)
        else:
            return JsonResponse(sorted_occurences)


if __name__ == "__main__":
    Ltechno = Loader("technologies.json")
    Ltechno.load_set()
    technologies = Ltechno.loaded_set

    Llang = Loader("languages.json")
    Llang.load_set()
    languages = Llang.loaded_set

    getter = DatabaseRecordsGetter()

    getter.count(technologies, "technologies", save=True)
    getter.count(languages, "languages", save=True)


