from django.shortcuts import render
from .forms import FilterForm, DataForm
from .models import JobOffer, JobPosition, Salary, Finances, Location
import json

def div_technologies(f_technologies):
    if f_technologies != None:
        f_technologies_list = f_technologies.split(",")
        for tech in f_technologies_list:
            tech.strip()
        return f_technologies_list
    return None

def joboffers(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }

    if request.method == 'POST':
        form = FilterForm(request.POST)

        f_technologies = form['technologies'].value()
        f_technologies_list = div_technologies(f_technologies)

        f_experience_level = form['experience_level'].value()

        f_b2b = form['b2b'].value()

        f_uop = form['uop'].value()

        f_address = form['address'].value()

        f_fork_min = form['fork_min'].value()
        try:
            f_fork_min = int(f_fork_min)
        except:
            f_fork_min = None

        f_fork_max = form['fork_max'].value()
        try:
            f_fork_max = int(f_fork_max)
        except:
            f_fork_max = None

        print(
            f' f_technologies: {f_technologies}'
            + f' f_experience_level: {f_experience_level}'
            + f' f_b2b: {f_b2b}'
            + f' f_uop: {f_uop}'
            + f' f_location: {f_address}'
            + f' f_fork_min: {f_fork_min}'
            + f' f_fork_max: {f_fork_max}'
        )

        offers = JobPosition.objects(
            technologies=f_technologies,
            experience_level__in=f_experience_level,
            finances__contracts__b2b=f_b2b,
            finances__contracts__uop=f_uop,
            location__address=f_address,
            finances__salary__b2b__min__gte=f_fork_min,
            finances__salary__b2b__max__lte=f_fork_max,
        )
        
        print(f'znalezione oferty: {offers}')
        # print(f'pierwsze.location {offers[0].location.address} , drugie.location {offers[1].location.address}')
        # print(f'pierwsze.location {offers[0].hash} , drugie.location {offers[1].hash}')
        context['offers'] = offers
    else:
        form = FilterForm()
        context['form'] = form
    return render(request, 'job_offers/content.html', context)



def json_dict_to_model(json_dict):
    job_offer = JobOffer()
    salary = Salary()
    location = Location()
    finances = Finances()
    job_offer['title'] = json_dict['title']
    location['address'] = json_dict['location']['address']
    #location['coordinates'] = json_dict['location']['coordinates']    for future
    job_offer['location'] = location
    job_offer['company'] = json_dict['company']
    job_offer['company_size'] = json_dict['company_size']
    job_offer['experience_level'] = json_dict['experience_level']
    job_offer['languages'] = json_dict['languages']
    job_offer['technologies'] = json_dict['technologies']
    salary['b2b'] = json_dict['finances']['salary']['b2b']
    salary['uop'] = json_dict['finances']['salary']['uop']
    finances['salary'] = salary
    finances['contracts'] = json_dict['finances']['contracts']
    job_offer['finances'] = finances
    job_offer['hash'] = json_dict['hash']
    job_offer['offer_link'] = json_dict['offer_link']
    job_offer['source_page'] = json_dict['source_page']
    job_offer.save()

def handle_uploaded_file(json_file):
    json_data = json_file.read()
    json_dict_list = json.loads(json_data)
    for json_dict in json_dict_list:
        json_dict_to_model(json_dict)

def file_upload(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }
    if request.method == 'POST':
        data_json = DataForm(request.POST, request.FILES)
        if data_json.is_valid():
            handle_uploaded_file(request.FILES['datafile'])
    else:
        data_json = DataForm()
        context['data_json'] = data_json
    return render(request, 'job_offers/file_upload_content.html', context)