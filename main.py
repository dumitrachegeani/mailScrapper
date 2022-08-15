import datetime
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List, Dict
from webdriver_manager.chrome import ChromeDriverManager
import os
import google
import utils
from google import search
from utils import Email
from utils import Phone

google_response_class = "yuRUbf"
ACCESSED_LINKS = set()
THREADS = 3
log_file = open('firms.log', 'a+')


# classes to be printed


def is_forbidden(link: str):
    for websites in utils.FORBIDDEN_WEBSITES:
        if websites in link:
            return True
    return False


# put relevant child links in the first five
def child_webdetails_sorted(passed_children_links: List['google.WebsiteDetails']):
    result_list = []
    for passed_child in passed_children_links:
        if 'contact' in passed_child.link or 'contact' in passed_child.description:
            result_list.append(passed_child)
        if 'info' in passed_child.link or 'info' in passed_child.description:
            result_list.append(passed_child)
        if 'despre' in passed_child.link or 'despre' in passed_child.description:
            result_list.append(passed_child)

    while len(result_list) < 5:
        if len(passed_children_links) == 0:
            return result_list
        else:
            result_list.append(passed_children_links.pop(0))

    return result_list[0:5]


# get all links from a specific google response
def get_children_of(driver: 'webdriver'):
    passed_children_links = []
    for element in driver.find_elements(By.TAG_NAME, 'a'):
        try:
            link = element.get_attribute('href')
            desc = element.text
            if desc is None:
                desc = 'None'
            forbidden = is_forbidden(link)
            not_accessed = link not in ACCESSED_LINKS
            if not forbidden and not_accessed:
                ACCESSED_LINKS.add(link)
                passed_children_links.append(google.WebsiteDetails(link, desc))
        except:
            continue
    return child_webdetails_sorted(passed_children_links)

# filter google response links and also get their children (sublinks)
def get_all_web_details_of(web_details: List['google.WebsiteDetails'], driver: 'webdriver'):
    passed_web_details = []
    for web_detail in web_details:
        # check for bad websites
        forbidden = is_forbidden(web_detail.link)
        not_accessed = web_detail.link not in ACCESSED_LINKS
        if not forbidden and not_accessed:
            passed_web_details.append(web_detail)
            ACCESSED_LINKS.add(web_detail.link)
            # get its children now
            driver.get(web_detail.link)
            children = get_children_of(driver)
            print('Got ' + str(len(children)) + ' children from ' + web_detail.link)
            passed_web_details.extend(children)
    print('Got a total of ' + str(len(passed_web_details)) + ' websites to search')
    return passed_web_details


# task to be run
def task(row, id_thread):
    # open output files for current thread
    output_emails = open(str(id_thread) + 'thread_emails.csv', 'a+')
    output_phones = open(str(id_thread) + 'thread_phones.csv', 'a+')

    # open the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.delete_all_cookies()

    for firm in row:
        firm = 'site:*.ro ' + firm
        all_emails: List[Email] = []
        all_phones: List[Phone] = []
        # google search firm
        search(driver, firm)
        print('Searching for firm ' + firm + '\n')
        # extract responses
        try:
            google_responses = driver.find_elements(By.CLASS_NAME, google_response_class)
        except:
            continue
        print('Got google responses')
        # convert webelement to webdetails object (link and description)
        website_details = google.web_element_to_website_details(google_responses)
        all_web_details = get_all_web_details_of(website_details, driver)
        # these are all web_details (all links and sublinks) for a specific firm
        for website in all_web_details:
            try:
                driver.get(website.link)
                print('Going to page ' + website.link)
                page_source = driver.page_source
            except:
                continue
            mails_from = utils.extract_mails_from(page_source, website.link)
            all_emails.extend(mails_from)
            phones_from = utils.extract_phones_from(page_source, website.link)
            all_phones.extend(phones_from)
            print('Got ' + str(len(mails_from)) + ' emails and ' + str(len(phones_from)) + ' phones from that page')
        print(all_emails)
        print(all_phones)
        compressed_emails = utils.compress_emails(all_emails)
        compressed_phones = utils.compress_phones(all_phones)
        print('Writing ' + str(len(compressed_emails)) + ' emails and ' + str(
            len(compressed_phones)) + ' phones for ' + firm)
        utils.writeEmails(output_emails, compressed_emails, firm)
        utils.writePhones(output_phones, compressed_phones, firm)


# put them 10 per row
def read_input():
    rows = []
    with open('input.csv') as f:
        for line in f:
            # strip whitespace
            line = line.strip()
            # separate the columns
            line = line.split(',')
            # divide it in 10 firms per row
            line_1 = line[0:10]
            line_2 = line[10:20]
            line_3 = line[20:30]
            line_4 = line[30:40]
            line_5 = line[40:50]
            rows.append(line_1)
            rows.append(line_2)
            rows.append(line_3)
            rows.append(line_4)
            rows.append(line_5)
    return rows


if __name__ == '__main__':

    switching_ip___ = str(datetime.datetime) + '- Finished ' + str(THREADS * 10) + ' firms, switching IP...'
    rows = read_input()

    # print(len(rows)) #2212 * 5
    MAX = len(rows)

    for i in range(0, MAX, THREADS):
        print(switching_ip___)
        log_file.write(switching_ip___)
        os.system('windscribe-cli connect')

        threads = []
        for thread_no in range(0, THREADS):
            thread = threading.Thread(target=task, args=(rows[i + thread_no], thread_no))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
