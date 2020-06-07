EXPERIENCE_CHOICES = (
    ('Junior', 'Junior'),
    ('Mid', 'Mid'),
    ('Senior', 'Senior'),
)

CONTRACT_NAME = {
    ('b2b', 'b2b'),
    ('uop','uop'),
}

def div_technologies(technologies):
    if technologies != None and technologies != '':
        technologies_list = [tech.strip() for tech in technologies.split(',') if tech.strip() != '']
        return technologies_list
    return None