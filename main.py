import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import google
import utils
from google import search

google_response_class = "yuRUbf"
ACCESSED_LINKS = set()
THREADS = 3


class Email:
    def __init__(self, email, site):
        self.email = email
        self.site = site
        self.count = 1


class Phone:
    def __init__(self, phone, site):
        self.phone = phone
        self.site = site
        self.count = 1


def task(row, id_thread):
    output_emails = open(str(id_thread) + 'thread_emails.csv', 'w+')
    output_phones = open(str(id_thread) + 'thread_phones.csv', 'w+')

    # opening the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.delete_all_cookies()

    for what_to_scrap in row:

        search(driver, what_to_scrap)
        # extract and filter responses
        try:
            google_responses = driver.find_elements(By.CLASS_NAME, google_response_class)
        except:
            continue
        website_details = google.web_element_to_website_details(google_responses)
        filtered_websites = utils.filter_websites(website_details)

        for website in filtered_websites:
            if website.link not in ACCESSED_LINKS:
                print(str(id_thread) + ') Minez site-ul ' + website.link)
                ACCESSED_LINKS.add(website.link)
                try:
                    driver.get(website.link)
                    page_source = driver.page_source
                except:
                    continue
                emails, phones = mine_from(page_source, website.link)
                utils.writeEmails(output_emails, emails, what_to_scrap)
                utils.writePhones(output_phones, phones, what_to_scrap)
                # mine subpages
                children_links = utils.extract_links_from(driver)

                for children in children_links:
                    if children.link not in ACCESSED_LINKS:
                        print('\t' + str(id_thread) + ') Minez site-ul ' + children.link)
                        ACCESSED_LINKS.add(children.link)
                        try:
                            driver.get(children.link)
                        except:
                            continue
                        page_source = driver.page_source
                        emails, phones = mine_from(page_source, children.link)
                        utils.writeEmails(output_emails, emails, what_to_scrap)
                        utils.writePhones(output_phones, phones, what_to_scrap)


def mine_from(page_source, link):
    emails = utils.extract_mails_from(page_source)
    email_objects = []
    for email in emails:
        added = False
        for email_object in email_objects:
            if email in email_object.email:
                email_object.count += 1
                added = True
                break
        if not added:
            email_objects.append(Email(email, link))

    phones1 = utils.extract_phones_from(page_source)
    phones = ['0' + str(phone) for phone in phones1]
    phone_objects = []
    for phone in phones:
        added = False
        for phone_object in phone_objects:
            if phone in phone_object.phone:
                phone_object.count += 1
                added = True
                break
        if not added:
            phone_objects.append(Phone(phone, link))
    return email_objects, phone_objects


if __name__ == '__main__':

    rows = []
    with open('input.csv') as f:
        for line in f:
            # strip whitespace
            line = line.strip()
            # separate the columns
            line = line.split(',')
            # save the line for use later
            rows.append(line)
    # print(len(rows)) 22129
    MAX = len(rows)
    for i in range(0, MAX, THREADS):
        threads = []
        print('Finished 150 firms, switching IP...')
        os.system('windscribe-cli connect "US Central"')

        for thread_no in range(0, THREADS):
            thread = threading.Thread(target=task, args=(rows[i+thread_no], thread_no))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
