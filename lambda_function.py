from bs4 import BeautifulSoup
import urllib.parse
import urllib

soup = None

def get_name_of_college(address):
    # Name of the university
    try:
        return soup.find('h1', {"class":'postcard__title'}).text.strip().replace("This college has been claimed by the college or a college representative.", "")
    except Exception as e:
        return "-"


def get_sat_range(address):
    # SAT Range
    try:
        for div in soup.find_all('div', 'scalar--three'):
            if 'SAT ' in div.text:
                return "SAT Range: " + div.text[9:]
    except urllib.error.URLError as e:
        return "SAT Range: " + "-"


def get_niche_grade(address):
    # The niche grade
    try:
        for div in soup.find_all('div', 'overall-grade__niche-grade'):
            return div.text
    except urllib.error.URLError as e:
        return "-"


def get_acceptance_rate(address):
    # The acceptance rate
    try:
        for item in soup.find(id='admissions'):
            for div in item.find_all('div', 'profile__bucket--1'):
                for x in div.find_all('div', 'scalar__value'):
                    return "Acceptance Rate: " + x.text
    except urllib.error.URLError as e:
        return "Acceptance Rate: " + "-"


def get_location(address):
    # The location of the college
    try:
        for span in soup.find_all('li', {"class":'postcard__attr postcard-fact'}):
            if ', ' in span.text:
                return "Location: " + span.text
    except urllib.error.URLError as e:
        return "Location: " + "-"


def get_cost(address):
    # The net cost
    try:
        for div in soup.find(id='cost'):
            for item in div.find_all('div', 'profile__bucket--1'):
                for item2 in item.find_all('div', 'scalar__value'):
                    avg, national = item2.text.split('/')
                    return "Net Price: " + avg
    except urllib.error.URLError as e:
        return "Net Price: " + "-"


def get_act_range(address):
    # Gets the ACT Range of the college selected
    try:
        for div in soup("div", "scalar--three"):
            if "ACT " in div.text:
                return "ACT Range: " + div.text[9:]

    except urllib.error.URLError as e:
        return "ACT Range: -"


def lambda_handler(event, context):
    college = event["search"]
    college = college.lower().replace(" ", "-")
    college = college.strip('.')
    address = "https://www.niche.com/colleges/" + college
    data = urllib.request.urlopen(address)
    data = data.read()

    global soup
    soup = BeautifulSoup(data, "html.parser")
    return {
        "message": {
            "Name": get_name_of_college(address),
            "Niche_Grade": get_niche_grade(address),
            "Sat_Range": get_sat_range(address),
            "Acceptance_Rate": get_acceptance_rate(address),
            "Location": get_location(address),
            "Net_Price": get_cost(address),
            "Act_Range": get_act_range(address)
        }
    }
