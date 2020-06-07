from common.utils import div_technologies
from common.models import JobPosition, Location, Finances, Salary
from datetime import date

def make_object_from_form(form):
    new_position = JobPosition()
    location = Location()
    finances = Finances()
    salary = Salary()

    location.address= form['location'].value()
    new_position.company_size = form['company_size'].value()

    try:
        new_position.experience_level = form['experience_level'].value()[0]
    except:
        new_position.experience_level = None

    new_position.technologies = div_technologies(form['technologies'].value())

    finances.contracts = {'b2b': False, 'uop': False}
    finances.contracts[form['contract'].value()] = True
    if 'b2b' == form['contract'].value():
        finances.contracts.b2b = True
        salary.b2b['min'] = form['fork_min'].value()
        salary.b2b['max'] = form['fork_max'].value()
    else:
        finances.contracts.uop = True
        salary.uop['min'] = form['fork_min'].value()
        salary.uop['max'] = form['fork_max'].value()

    new_position.date = str(date.today())

    new_position.location = location
    finances.salary = salary
    new_position.finances = finances

    # # for debugging
    # print('Succesfuly created new position')
    # print('Adres: ', new_position.location.address)
    # print('Company size: ', new_position.company_size)
    # print('Experience Level: ', new_position.experience_level)
    # print('Technologies: ', new_position.technologies)
    # print('Contracts: ', new_position.finances.contracts)
    # print('b2b: ', new_position.finances.salary.b2b)
    # print('uop: ', new_position.finances.salary.uop)
    # print('Date: ', new_position.date)

    return new_position