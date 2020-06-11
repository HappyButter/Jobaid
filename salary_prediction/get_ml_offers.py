from job_offers.models import JobOffer
import json
from mongoengine.queryset.visitor import Q


def make_ml_offers_list():
    query = (
        Q(finances__salary__b2b__min__ne=None) 
        & Q(finances__salary__b2b__max__ne=None) 
        & Q(finances__salary__b2b__min__ne=0) 
        & Q(finances__salary__b2b__max__ne=0)
    ) | (
        Q(finances__salary__uop__min__ne=None) 
        & Q(finances__salary__uop__max__ne=None) 
        & Q(finances__salary__uop__min__ne=0) 
        & Q(finances__salary__uop__max__ne=0)
    )

    offers = [offer for offer in JobOffer.objects(query)]

    __test_amount_of_offers(offers) # for debugging

    data_b2b = _get_ml_data_from_offer_b2b(offers)
    with open('ml_output_b2b_CSizeNone.json','w') as outfile:
        json.dump(data_b2b, outfile)

    data_uop = _get_ml_data_from_offer_uop(offers)
    with open('ml_output_uop_CSizeNone.json','w') as outfile:
        json.dump(data_uop, outfile)

    average_company_size = _clculate_average_company_size(offers)
    data_b2b_average = _get_ml_data_from_offer_b2b(offers, average_company_size)
    with open('ml_output_b2b_CSizeAverage.json','w') as outfile:
        json.dump(data_b2b_average, outfile)

    data_uop_average = _get_ml_data_from_offer_uop(offers, average_company_size)
    with open('ml_output_uop_CSizeAverage.json','w') as outfile:
        json.dump(data_uop_average, outfile)

    # for debugging
    print('With null:')
    print('Number of offers with b2b: ', len(data_b2b))
    print('Number of offers with uop: ', len(data_uop))
    print('Offers with uop and b2b is: ', len(data_b2b) + len(data_uop) - len(offers))
    print('With average (amounts should be the same):')
    print('Number of offers with b2b: ', len(data_b2b_average))
    print('Number of offers with uop: ', len(data_uop_average))
    print('Offers with uop and b2b is: ', len(data_b2b_average) + len(data_uop_average) - len(offers))


def _b2b_salary_not_exist(offer):
    return offer.finances.salary.b2b['min'] == None or offer.finances.salary.b2b['min'] == 0 or offer.finances.salary.b2b['max'] == None or offer.finances.salary.b2b['max'] == 0

def _uop_salary_not_exist(offer):
    return offer.finances.salary.uop['min'] == None or offer.finances.salary.uop['min'] == 0 or offer.finances.salary.uop['max'] == None or offer.finances.salary.uop['max'] == 0

def _get_ml_data_from_offer_b2b(offers, company_size=None):
    data = []
    
    for offer in offers:

        offer_data = _get_common_ml_data_from_offer(offer)
        offer_data['company_size'] = company_size

        if _b2b_salary_not_exist(offer):
            pass
        else:
            offer_data['salary'] = int((offer.finances.salary.b2b['min'] + offer.finances.salary.b2b['max']) / 2)
            data.append(offer_data)

    return data

def _get_ml_data_from_offer_uop(offers, company_size=None):
    data = []

    for offer in offers:

        offer_data = _get_common_ml_data_from_offer(offer)
        offer_data['company_size'] = company_size

        if _uop_salary_not_exist(offer):
            pass
        else:
            offer_data['salary'] = int((offer.finances.salary.uop['min'] + offer.finances.salary.uop['max']) / 2)
            data.append(offer_data)

    return data

def _get_common_ml_data_from_offer(offer):

    offer_data = {}

    offer_data['experience_level'] = offer.experience_level
    offer_data['languages'] = offer.languages
    offer_data['technologies'] = offer.technologies
    offer_data['location'] = offer.location.address

    return offer_data

def _clculate_average_company_size(offers):
    company_size_sum = 0
    company_size_quantity = 0

    for offer in offers:
        if offer.company_size != None:
            company_size_sum += offer.company_size
            company_size_quantity += 1

    return int(company_size_sum/company_size_quantity)


def __print_salaries_and_title(offervv, indexrf = None):
    if indexrf != None:
        print(f'[{indexrf}] ', offervv.title)
    else:
        print(offervv.title)

    print(' b2b min: ', offervv.finances.salary.b2b['min'])
    print(' b2b max: ', offervv.finances.salary.b2b['max'])
    print(' uop min: ', offervv.finances.salary.uop['min'])
    print(' uop max: ', offervv.finances.salary.uop['max'])

def __print_all_salaries(offersss):
    for indexrfs, offervvs in enumerate(offersss):
        _print_salaries_and_title(offervvs, indexrfs)

def __test_amount_of_offers(offers):

    print('Number of all offers: ', len(offers))

    ile_common = 0
    for offer in offers:
        if offer.finances.salary.b2b['min'] == None or offer.finances.salary.b2b['min'] == 0:
            pass
        elif offer.finances.salary.uop['min'] == None or offer.finances.salary.uop['min'] == 0:
            pass
        else:
            ile_common += 1
            
    print('commmon amount = ', ile_common)

    ile_b2b = 0
    for offer in offers:
        if offer.finances.salary.b2b['min'] == None or offer.finances.salary.b2b['min'] == 0:
            pass
        else:
            ile_b2b += 1
            
    print('b2b amount = ', ile_b2b)


    ile_uop = 0
    for offer in offers:
        if offer.finances.salary.uop['min'] == None or offer.finances.salary.uop['min'] == 0:
            pass
        else:
            ile_uop += 1
            
    print('uop amount = ', ile_uop)

    print('Do this numbers add together correctly?:', ( ile_b2b + ile_uop - ile_common - len(offers) ) == 0)

    print('####################################################################')