import random
import re
import time
import phonenumbers
from selenium.webdriver.common.by import By

import google

FORBIDEN_WEBSITES = [
    "listafirme.ro/",
    "termene.ro/",
    "indaco.ro/",
    "lege5.ro",
    "totalfirme.ro/",
    "expose.ro/",
    "confidas.ro/",
    "lista-firme-romania.ro/",
    "cloudflare.com",
    "romanian-companies.eu/"
]
FORBIDEN_MAIL_WORDS = [
    ".png",
    ".jpg",
    ".jpeg",
    "Dpo",
    "Dataprotection",
    "Anaf",
    "Gov",
    "Ambasada",
    "Politie",
    "Politia",
    "Primarie",
    "Courier",
    "Curier",
    "Dpd",
    "Cargus"
]


def delay():
    time.sleep(random.randrange(2, 5))


def writeToCsvRow(f, list):
    for elem in list:
        try:
            f.write(elem + ',')
        except:
            print("unicode error")
    f.write('\n')


def writeEmails(f, all_emails, firm):
    for email in all_emails:
        # try:
        f.write(firm + ',' + email.email + ',' + str(email.count) + ',' + email.site + '\n')
        # except:
        #     print("unicode error")
        # f.write('\n')
    f.flush()


def writePhones(f, all_phones, firm):
    for phone in all_phones:
        # try:
        f.write(str(firm) + ',' + str(phone.phone) + ',' + str(phone.count) + ',' + str(phone.site) + '\n')
        # except:
        #     print("unicode error")
        # f.write('\n')
    f.flush()


def filter_websites(website_details):
    filtered_websites = []
    for website_detail in website_details:
        link: str = website_detail.link
        if not any(word in link for word in FORBIDEN_WEBSITES):
            filtered_websites.append(website_detail)
    return filtered_websites


def not_forbidden(email):
    for word in FORBIDEN_MAIL_WORDS:
        if word in email:
            return False
    return True


def extract_mails_from(page_source):
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', page_source)
    return filter(lambda email: not_forbidden(email), emails)


def extract_phones_from(page_source):
    return [match.number.national_number for match in phonenumbers.PhoneNumberMatcher(page_source, "RO")]


# returns the list of WensiteDetails from the first links
def extract_links_from(driver):
    good_words = ['contact', 'despre', 'informati', 'ajutor']
    list = []
    ordered_list = []
    for link in driver.find_elements(By.TAG_NAME, 'a'):
        try:
            href = link.get_attribute('href')
            text = link.text
        except:
            continue
        if href is None or text is None:
            continue
        list.append(google.WebsiteDetails(href, text))
    for item in list:
        for word in good_words:
            if word in item.link:
                ordered_list.append(item)
    return list[:5]
