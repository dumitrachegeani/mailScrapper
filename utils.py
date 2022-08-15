import re
from typing import List, Dict
import phonenumbers

FORBIDDEN_WEBSITES = [
    "listafirme",
    "termene",
    "indaco",
    "lege5.ro",
    "totalfirme",
    "expose",
    "confidas",
    "lista-firme-romania",
    "cloudflare.com",
    "romanian-companies",
    'mail',
    'risco.ro/autentificare,',
    'risco.ro/cont-nou',
    'risco.ro/rapoarte-bonitate',
    'paginiaurii.ro/contact/',
    'aginiaurii.ro/despre-noi',
    'paginiaurii.ro/despre-noi-videoclip',
    'paginiaurii.ro/',

]
FORBIDDEN_MAIL_WORDS = [
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


class Email:
    def __init__(self, email, link):
        self.email = email
        self.link = link
        self.count = 1

    def __str__(self):
        return self.email + ',' + str(self.count) + ',' + self.link

    def __repr__(self):
        return self.__str__()


class Phone:
    def __init__(self, phone, link):
        self.phone = phone
        self.link = link
        self.count = 1

    def __str__(self):
        return self.phone + ',' + str(self.count) + ',' + self.link

    def __repr__(self):
        return self.__str__()


def writeEmails(f, all_emails, firm):
    for email in all_emails:
        f.write(email.__str__() + '\n')
    f.flush()


def writePhones(f, all_phones, firm):
    for phone in all_phones:
        f.write(phone.__str__() + '\n')
    f.flush()


def not_forbidden(email):
    for word in FORBIDDEN_MAIL_WORDS:
        if word in email:
            return False
    return True


def extract_mails_from(page_source, link):
    result = []
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', page_source)
    for email in emails:
        if not_forbidden(email):
            result.append(Email(email, link))
    return result


def extract_phones_from(page_source, link):
    return [Phone('0' + str(number), link) for number in
            [match.number.national_number for match in phonenumbers.PhoneNumberMatcher(page_source, "RO")]]


def compress_emails(all_emails: List['Email']):
    email_map: Dict[str, Email] = dict()
    final_list = []
    for email in all_emails:
        if email.email not in email_map:
            email_map[email.email] = email
            final_list.append(email)
        else:
            email_map[email.email].count += 1
    return final_list


def compress_phones(all_phones: List['Phone']):
    phone_map: Dict[str, Phone] = dict()
    final_list = []
    for phone in all_phones:
        if phone.phone not in phone_map:
            phone_map[phone.phone] = phone
            final_list.append(phone)
        else:
            phone_map[phone.phone].count += 1
    return final_list
