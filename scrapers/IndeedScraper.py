import re
import sys
import json
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from hashlib import blake2b
from bs4 import BeautifulSoup
from datetime import date, timedelta


DEST_FOLDER = "scraped_data/"
SOURCE_FOLDER = "info/"

languages = [
            "Assembler",
            "Pascal",
            "Elixir",
            "CSS3",
            "HTML",
            "NoSQL",
            "Python",
            "Ruby",
            "C#",
            "Fortran",
            "Lisp",
            "Matlab"
            "Objective-C",
            "HTML5",
            "SCSS",
            "Erlang",
            "PHP",
            "Kotlin",
            "Rust",
            "Flutter",
            "Julia",
            "CSS",
            "C++",
            "Golang",
            "TypeScript",
            "JavaScript",
            "VBA",
            "Dart"
        ]

exceptional_languages = ["C",
                         "R",
                         "Swift",
                         "Scala",
                         "Go",
                         "Java",
                         "SQL",
                         "Lua"]


def load_data(filename):
    with open(filename, "r") as file:
        technologies = json.load(file)
    return technologies

technologies = load_data(SOURCE_FOLDER + "technologies.json")
exceptional_technologies = load_data(SOURCE_FOLDER + "exceptional_technologies.json")

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
                return [int(digits[0] + digits[1]), int(digits[2] + digits[3])], None
            elif len(digits) == 2:
                return [int(digits[0]), int(digits[1])], None

    if "b2b" in salary_line_lower:
        salary_line_lower = salary_line_lower.replace("b2b", "")
        digits = re.findall(r"\d+", salary_line_lower)
        if len(digits) == 4:
            return None, [int(digits[0] + digits[1]), int(digits[2] + digits[3])]
        elif len(digits) == 2:
            return None, [int(digits[0]), int(digits[1])]

    return None, None


def double_contract_salary_handler(text):
    uop_number = text.find("uop")
    b2b_number = text.find("b2b")

    text = text.replace("b2b", "")
    digits = re.findall(r"\d+", text)

    if uop_number < b2b_number:
        if len(digits) == 8:
            return [int(digits[0] + digits[1]), int(digits[2] + digits[3])
                    ], [int(digits[4] + digits[5]), int(digits[6] + digits[7])]
        else:
            return None, None

    if b2b_number < uop_number:
        if len(digits) == 8:
            return [int(digits[4] + digits[5]), int(digits[6] + digits[7])
                    ], [int(digits[0] + digits[1]), int(digits[2] + digits[3])]
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
    opt = Options()
    # opt.add_argument("--headless")
    browser = webdriver.Firefox(executable_path=PATH, options=opt)

    regex_formula_salary = r"(?i)^.*\b(Salary)\b.*$"
    regex_formula_company_size = r"(?i)^.*\b(Company size)\b.*$"

    page_links = ["https://pl.indeed.com/praca?q=java&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=c%2B%2B&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=python&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=javascript&sort=date&radius=25&start=",
                  "https://pl.indeed.com/praca?q=go+developer&sort=date&radius=25&start="]

    data_json = ["java.json", "c++.json", "python.json", "js.json", "go.json"]


    # for index, page_link in enumerate(page_links):
    #     save_to_json(gather_data(
    #         browser,
    #         page_link,
    #         regex_formula_company_size,
    #         regex_formula_salary
    #     ), DEST_FOLDER + data_json[index])
    save_to_json(gather_data(
        browser,
        page_links[4],
        regex_formula_company_size,
        regex_formula_salary
    ), DEST_FOLDER + data_json[4])

    browser.quit()


def gather_data(
    browser,
    page_link,
    regex_formula_company_size,
    regex_formula_salary
):
    offers = []
    browser.get(page_link + str(0))
    pages = browser.find_element_by_id("searchCountPages").text
    max_page = extract_max_page(pages)
    n_offers  = 0

    current_page_number = -1
    for offer in range(0, 10*(max_page-1), 10): #x 10
    # for offer in range(0, 10, 10):

        browser.get(page_link + str(offer))
        all_jobs = browser.find_elements_by_class_name("result")

        pages = browser.find_element_by_id("searchCountPages").text
        if current_page_number == extract_current_page(pages):
            break

        current_page_number = extract_current_page(pages)

        for index, job in enumerate(all_jobs):
            job_offer = scrap(job, browser,
                                    regex_formula_company_size,
                                    regex_formula_salary)
            if index == 0:
                offers.append(job_offer)
                n_offers +=1
            elif index !=0 and offers[index - 1]["hash"] != job_offer["hash"]:
                offers.append(job_offer)
                n_offers += 1


    print(f"Collected offers: {n_offers}")
    return offers


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
    try:
        contracts = handle_contracts(title, job_desc)
    except:
        contracts = None
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

    try:
        uop, b2b = description_salary_seeker(description_salary)
        uop, b2b = decide_where_to_pass_min_max(min, max, uop, b2b, contracts)
    except:
        uop = None
        b2b = None

    if uop and (uop[0] < 1000 or uop[0] > 60000 or uop[1] < 1000 or uop[1] > 60000):
        uop = None

    if b2b and (b2b[0] < 1000 or b2b[0] > 60000 or b2b[1] < 1000 or b2b[1] > 60000):
        b2b = None
    # Handling the "offer_link" field
    try:
        offer_link = "https://pl.indeed.com/viewjob?jk=" + extract_offer_code(soup)
    except:
        offer_link = None

    # Handling the "active" field
    try:
        offer_status = browser.find_element_by_class_name("date ").text
        try:
            offer_age = int(number_extractor_from_line(offer_status))
        except:
            offer_age = 0
    except:
        offer_status = None
        offer_age = None

    if offer_status == None or "30+" in offer_status:
        active = False
    else:
        active = True

    # Handling "company_size" field
    try:
        company_size = find_company_size(regex_formula_company_size, job_desc)
    except:
        company_size = None
    # Handling the "position level" field
    try:
        position_level = handle_position_level(title, job_desc)
    except:
        position_level = None
    # Handling the "languages" field
    try:
        position_languages = handle_languages(title, job_desc)
    except:
        position_languages = None
    # Handling the "technologies" list
    try:
        position_technologies = handle_technologies(title, job_desc)
    except:
        position_technologies = None
    # print(job_desc)

    return pass_vars_to_dict(
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
        offer_age,
        active
    )



def handle_contracts(title, job_desc):
    contracts = find_words_in_text(title, contracts_list)
    if not contracts and job_desc != None:
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
        offer_age,
        active):

    offer = {"title": title,
             "company": company,
             "company_size": int(company_size[0]) if company_size else None,
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
                 "salary": {
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

    offer["offer_hash"] = __generate_offer_hash(offer)
    offer["offer_link"] = offer_link
    offer["source_page"] = "indeed.com"
    offer["date"] = date.today() - timedelta(days=offer_age) if offer_age != None else date.today() - timedelta(days=30)
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
    if job_desc == None:
        return None
    return re.findall(r"\d+",
                      find_regex(
                          re.finditer(
                              regex_formula_company_size, job_desc, re.MULTILINE)
                      )
                      )


def save_to_json(data_json, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, separators=(',', ':'), default=str)


def decide_where_to_pass_min_max(min, max, uop, b2b, contracts):
    if min and max and contracts:
        if "b2b" in contracts and not uop:
            if "uop" in contracts:
                return uop, b2b
            return uop, [int(min), int(max)]
        elif "uop" in contracts and not uop:
            return [int(min), int(max)], b2b

    return uop, b2b


if __name__ == "__main__":
    seeker()

