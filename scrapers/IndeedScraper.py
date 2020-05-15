import re
import sys
import json
import math
import pandas as pd
from selenium import webdriver
from hashlib import blake2b
from bs4 import BeautifulSoup


languages = ['C#',
             'C++',
             'Python',
             'Javascript',
             'Typescript',
             'PhP',
             'Ruby on rails',
             'Html5',
             'Html',
             'CSS3',
             'SCSS',
             'SASS',
             'CSS',
             'Kotlin',
             'Swift',
             'Flutter',
             'Scala',
             'Rust',
             'Vba',
             'Ruby',
             'Objective-C',
             'NoSQL',
             'Dart',
             'Golang',
             'PhP 7',
             'Julia',
             'Elixir',
             'Erlang']

exceptional_languages = ["C",
                         "R",
                         "Lua",
                         "Go",
                         "Java",
                         "SQL",
                         "Lua"]

technologies = ["Android", "Maven", "CMake", "Node.js", "Vue.js",
                "MongoDB", "autostar", "TCP/IP", "Scrum",
                "Deep Learning", "Bitbucket", "Jenkins",
                "Jira", "Confluence", "Docker", "Mesos", "C++11", "C++17", "C++14",
                "C++20", "C++11/14/17", "Kubernetes", "SDN/NFV",
                "Bamboo", "Windows Server", "SQL Server", "JQuery", "Linux",
                "Angular", "HTML5", "ASP.NET", "CSS", ".NET", "DevOps",
                ".NET Core", "SaaS", "Perforce", "Unity2D", "Unity3D",
                "Unity", "Unreal Engine", "PostgreSQL", "Unix", "MySQL", "Mercirual",
                "XML", "SpringBoot", "Spring", "automated tests", "writing tests",
                "Tomcat", "Hibernate", "GoCD", "Webmethod", "Oracle", "IntelliJ",
                "WinForms", "Assembler", "Assembly", "Azure", "Hadoop", "OpenCV",
                "Electron", "Computer Vision", "machine learning"]

exceptional_technologies = ["SQL",
                            "AI",
                            "ML",
                            "OSI",
                            "AWS",
                            "SED",
                            "AWK",
                            "Qt",
                            "Git",
                            "CI",
                            "TDD",
                            "STL",
                            "REST",
                            "TFS",
                            "Vue",
                            "React",
                            "Agile",
                            "Shell", ]

contracts_list = [
    "b2b",
    "uop"]

position_levels = ["junior", "mid", "senior"]


def number_extractor_from_line(str):
    return re.sub(r"\D", "", str)


# Salary Seeker functions:

def description_salary_seeker(salary_line):

    if salary_line is None:
        return None, None

    salary_line_lower = salary_line.replace(".", " ").replace("k","00").replace(",", " ").lower()

    if "uop" in salary_line_lower:
        if "b2b" in salary_line_lower:
            return double_contract_salary_handler(salary_line_lower)
        else:
            digits = re.findall(r"\d+", salary_line_lower)
            if len(digits) == 4:
                return [digits[0] + digits[1], digits[2] + digits[3]], None
            elif len(digits) == 2:
                return [digits[0], digits[1]], None

    if "b2b" in salary_line_lower:
        salary_line_lower = salary_line_lower.replace("b2b", "")
        digits = re.findall(r"\d+", salary_line_lower)
        if len(digits) == 4:
            return None, [digits[0] + digits[1], digits[2] + digits[3]]
        elif len(digits) == 2:
            return None, [digits[0], digits[1]]

    return None, None


def double_contract_salary_handler(text):
    uop_number = text.find("uop")
    b2b_number = text.find("b2b")

    text = text.replace("b2b", "")
    digits = re.findall(r"\d+", text)

    if uop_number < b2b_number:
        if len(digits) == 8:
            return [digits[0] + digits[1], digits[2] + digits[3]
                    ], [digits[4] + digits[5], digits[6] + digits[7]]
        else:
            return None, None

    if b2b_number < uop_number:
        if len(digits) == 8:
            return [digits[4] + digits[5], digits[6] + digits[7]
                    ], [digits[0] + digits[1], digits[2] + digits[3]]
        else:
            pass

    return None, None  # unhandled cases

############


def c_languages_examinator(languages):
    if "C++" in languages and "C" in languages:
        languages.remove("C++")
        languages.remove("C")
        languages.append("C/C++")

    return languages


def find_words_in_text(description, words):
    found = []
    text = description.lower()
    for word in words:
        if word.lower() in text:
            found.append(word)
        else:
            continue

    return found


def find_exceptional_words_in_text(text, words):
    lang = []
    text = text.lower().replace("/", " ").split()
    for word in words:
        for string in text:
            if word.lower() == string.strip(",.()/"):
                lang.append(word)
                break
            else:
                continue
    return lang


def find_salary(text):
    maxList = []
    minList = []
    minmax = text.split("-")
    for char in list(minmax[0]):
        if char.isdigit():
            minList.append(char)
            min = int("".join(minList))

    for char in list(minmax[1]):
        if char.isdigit():
            maxList.append((char))
            max = int("".join(maxList))

    return min, max


def find_regex(matches):
    f_matches = []
    for match in matches:
        f_matches.append(match.group())
    return ", ".join(f_matches)


def __generate_offer_hash(offer):
    string = json.dumps(offer, sort_keys=True)
    h = blake2b(digest_size=30)
    h.update(string.encode('utf-8'))

    return h.hexdigest()


def extract_max_page(pages):
    number_str = "".join(re.findall(r"\d+", pages.split("-")[1]))
    return math.ceil(float(number_str) / 10.)


def extract_current_page(pages):
    return int(re.findall(r"\d+", pages.split("-")[0])[0])


def seeker():
    PATH = "/home/mateusz/browserScrapingDrivers/geckodriver"
    browser = webdriver.Firefox(executable_path=PATH)

    regex_formula_salary = r"(?i)^.*\b(Salary)\b.*$"
    regex_formula_company_size = r"(?i)^.*\b(Company size)\b.*$"

    page_links = ["https://pl.indeed.com/praca?q=java&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=c%2B%2B&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=python&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=javascript&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=go+developer&sort=date&radius=25&start="]

    data_json = []

    for page_link in page_links:
        data_json.append(gather_data(
            browser,
            page_link,
            regex_formula_company_size,
            regex_formula_salary
        ))

    browser.quit()
    save_to_json(data_json)


def gather_data(
    browser,
    page_link,
    regex_formula_company_size,
    regex_formula_salary
):
    data_json = []

    browser.get(page_link + str(0))
    pages = browser.find_element_by_id("searchCountPages").text
    max_page = extract_max_page(pages)
    n_offers  = 0

    current_page_number = -1
    # for offer in range(0, max_page-1, 1): #x 10
    for offer in range(0, 10, 10):

        browser.get(page_link + str(offer))
        all_jobs = browser.find_elements_by_class_name("result")

        pages = browser.find_element_by_id("searchCountPages").text
        if current_page_number == extract_current_page(pages):
            break

        current_page_number = extract_current_page(pages)

        for job in all_jobs:
            data_json.append(scrap(job, browser,
                                    regex_formula_company_size,
                                    regex_formula_salary))
            n_offers += 1

    print(f"Collected offers: {n_offers}")
    return data_json


def scrap(
    job,
    browser,
    regex_formula_company_size,
    regex_formula_salary
):

    result_html = job.get_attribute("innerHTML")
    soup = BeautifulSoup(result_html, "html.parser")

    min = None
    max = None

    # Auto colsing of pop-up windows and clicking on the offer
    sum_div = job.find_elements_by_class_name("summary")[0]
    try:
        sum_div.click()
    except:
        close_button = browser.find_elements_by_class_name(
            "popover-x-button-close")[0]
        close_button.click()
        sum_div.click()

    # Handling the "title" field
    try:
        title = soup.find("a", class_="jobtitle").text.replace("\n", "")
    except:
        title = None

    # Hangling the "location" field
    try:
        location = soup.find(class_="location").text
    except:
        location = None

    # Handling the "company" field
    try:
        company = soup.find(class_="company").text.replace("\n", "").strip()
    except:
        company = None

    # Extraction of job description
    try:
        job_desc = soup.find(class_="vjs-desc").text
    except :
        try:
            job_desc = browser.find_element_by_id("vjs-desc").text
        except:
            job_desc = None

    # Handling the "contracts" field
    contracts = handle_contracts(title, job_desc)

    # Handling the "salary" field
    try:
        salary = soup.find(class_="salaryText").text.replace("\n", "").strip()
        min, max = find_salary(salary)
    except:
        salary = None

    try:
        description_salary = next(
            re.finditer(
                regex_formula_salary,
                job_desc,
                re.MULTILINE)).group()
    except:
        description_salary = None

    if not description_salary:
        description_salary = None

    uop, b2b = description_salary_seeker(description_salary)
    uop, b2b = decide_where_to_pass_min_max(min, max, uop, b2b, contracts)

    # Handling the "offer_link" field
    offer_link = "https://pl.indeed.com/viewjob?jk=" + extract_offer_code(soup)


    # Handling the "active" field
    try:
        offer_status = browser.find_element_by_class_name("date ").text
    except:
        offer_status = None

    if "30+" in offer_status or offer_status is None:
        active = False
    else:
        active = True

    # Handling "company_size" field
    company_size = find_company_size(regex_formula_company_size, job_desc)

    # Handling the "position level" field
    position_level = handle_position_level(title, job_desc)

    # Handling the "languages" field
    position_languages = handle_languages(title, job_desc)

    # Handling the "technologies" list
    position_technologies = handle_technologies(title, job_desc)

    # print(job_desc)

    offer = pass_vars_to_dict(
        title,
        company,
        company_size,
        location,
        position_level,
        position_languages,
        position_technologies,
        contracts,
        b2b,
        uop,
        offer_link,
        active
    )

    return offer


def handle_contracts(title, job_desc):
    contracts = find_words_in_text(title, contracts_list)
    if not contracts:
        contracts = find_words_in_text(job_desc, contracts_list)
    if not contracts:
        contracts = None

    return contracts


def pass_vars_to_dict(
        title,
        company,
        company_size,
        location,
        position_level,
        position_languages,
        position_technologies,
        contracts,
        b2b,
        uop,
        offer_link,
        active):

    offer = {"title": title,
             "company": company,
             "company_size": company_size if company_size else None,
             "location": {
                 "address": location,
             },
             "experience_level": position_level,
             "languages": position_languages,
             "technologies": position_technologies,
             "finances": {
                 "contracts": {
                     "b2b": True if (contracts and "b2b" in contracts) or b2b else False,
                     "uop": True if (contracts and "uop" in contracts) or uop else False,
                 },
                 "salary:": {
                     "b2b": {
                         "min": b2b[0] if b2b else None,
                         "max": b2b[1] if b2b else None
                     },
                     "uop": {
                         "min": uop[0] if uop else None,
                         "max": uop[1] if uop else None
                     }
                 }
             }
             }

    offer["hash"] = __generate_offer_hash(offer)
    offer["offer_link"] = offer_link
    offer["source_page"] = "indeed"
    offer["active"] = active

    return offer


def extract_offer_code(soup):
    return soup.a['id'].replace("jl_", "")


def handle_technologies(title, job_desc):
    position_technologies_list = find_words_in_text(job_desc, technologies)
    position_exceptional_technologies_list = find_exceptional_words_in_text(
        job_desc, exceptional_technologies)

    if not position_technologies_list:
        position_technologies_list = find_words_in_text(title, technologies)

    position_technologies_list += position_exceptional_technologies_list

    return position_technologies_list


def handle_languages(title, job_desc):
    position_languages_list = find_words_in_text(title, languages)
    position_exceptional_languages_list = find_exceptional_words_in_text(
        job_desc, exceptional_languages)

    if not position_exceptional_languages_list:
        position_exceptional_languages_list = find_exceptional_words_in_text(
            title, exceptional_languages)
    if not position_languages_list:
        position_languages_list = find_words_in_text(job_desc, languages)

    position_languages_list += position_exceptional_languages_list

    return position_languages_list


def handle_position_level(title, job_desc):
    position_level = "".join(find_words_in_text(title, position_levels))
    if not position_level:
        position_level = "".join(find_words_in_text(job_desc, position_levels))
    if not position_level:
        position_level = None

    return position_level


def find_company_size(regex_formula_company_size, job_desc):
    return re.findall(r"\d+",
                      find_regex(
                          re.finditer(
                              regex_formula_company_size, job_desc, re.MULTILINE)
                      )
                      )


def save_to_json(data_json):
    with open("indeed.json", "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)


def decide_where_to_pass_min_max(min, max, uop, b2b, contracts):
    if min and max and contracts:
        if "b2b" in contracts and not uop:
            if "uop" in contracts:
                return uop, b2b
            return uop, [min, max]
        elif "uop" in contracts and not uop:
            return [min, max], b2b

    return uop, b2b


if __name__ == "__main__":
    seeker()

