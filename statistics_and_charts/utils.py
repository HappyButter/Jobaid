from  job_offers.models import JobPosition
from .models import ChartsData
from datetime import date

def recalculate_statistics():
    new_data = ChartsData()
    new_data.company_size = company_size()
    new_data.experience_level = level()
    new_data.contracts = constracts()
    new_data.languages = languages()
    new_data.technologies = technologies()
    new_data.date = date.today()

    # temporary for debugging
    # print('languages: ', new_data.languages)
    # print('company_size: ', new_data.company_size)
    # print('experience level:', new_data.experience_level)
    # print('contracts:', new_data.contracts)
    # print('technologies: ', new_data.technologies)

    new_data.save()


def languages():
    offers = JobPosition.objects() 
    stats = {
        'JavaScript': 0,
        'Python': 0,
        'Java': 0,
        'C#': 0,
        'PHP': 0,
        'C++': 0,
        'Others': 0
    }
    
    for offer in offers:
        lowercase_languages = [lang.lower() for lang in offer['languages']]
        if 'javascript' in lowercase_languages:
            lowercase_languages.remove('javascript')
            stats['JavaScript'] += 1
        if 'python' in lowercase_languages:
            lowercase_languages.remove('python')
            stats['Python'] += 1
        if 'java' in lowercase_languages:
            lowercase_languages.remove('java')
            stats['Java'] += 1
        if 'c#' in lowercase_languages:
            lowercase_languages.remove('c#')
            stats['C#'] += 1
        if 'php' in lowercase_languages:
            lowercase_languages.remove('php')
            stats['PHP'] += 1
        if 'c++' in lowercase_languages:
            lowercase_languages.remove('c++')
            stats['C++'] += 1
        
        if len(lowercase_languages) > 0:
            stats['Others'] += 1

    return stats


def level():
    offers = JobPosition.objects() 
    stats = {
        'junior' : 0,
        'mid' : 0,
        'senior' : 0
    }
    
    for offer in offers:
        experience_level = offer['experience_level']
        if 'junior' == experience_level:
            stats['junior'] += 1
        if 'mid' == experience_level:
            stats['mid'] += 1
        if 'senior' == experience_level:
            stats['senior'] += 1

    return stats


def technologies():
    offers = JobPosition.objects() 
    stats = {
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
    
    for offer in offers:
        technologies = [tech.lower() for tech in offer['technologies']]
        if 'docker' in technologies:
            stats['Docker'] += 1
        if 'aws' in technologies:
            stats['AWS'] += 1
        if 'angular' in technologies:
            stats['Angular'] += 1
        if 'spring' in technologies:
            stats['Spring'] += 1
        if 'react' in technologies:
            stats['React'] += 1
        if 'kubernetes' in technologies:
            stats['Kubernetes'] += 1
        if '.net' in technologies:
            stats['.NET'] += 1
        if 'node.js' in technologies or 'nodejs' == technologies or 'node' == technologies:
            stats['Node.js'] += 1
        if 'mysql' in technologies:
            stats['MySQL'] += 1

    return stats
    

def constracts():
    offers = JobPosition.objects() 
    stats = {
        'b2b' : 0,
        'uop' : 0
    }
    
    for offer in offers:
        constract = offer['finances']['contracts']
        if constract['b2b']:
            stats['b2b'] += 1
        if constract['uop']:
            stats['uop'] += 1

    return stats


def company_size():
    offers = JobPosition.objects() 
    stats = {
        '<10' : 0,
        '10-50' : 0,
        '50-200' : 0,
        '200-500': 0,
        '500-1000': 0,
        '>1000': 0
    }
    
    for offer in offers:
        size = offer['company_size']
        
        if size != None:
            if size <= 10:
                stats['<10'] += 1
            if size > 10 and size <= 50:
                stats['10-50'] += 1
            if size > 50 and size <= 200:
                stats['50-200'] += 1
            if size > 200 and size <= 500:
                stats['200-500'] += 1
            if size > 500 and size <= 1000:
                stats['500-1000'] += 1
            if size > 1000:
                stats['>1000'] += 1
    return stats
    