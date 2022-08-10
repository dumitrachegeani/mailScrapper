import random
import time

FORBIDEN_WORDS = [
    'listafirme'
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

def filter_websites(website_details):
    filtered_websites = []
    for website_detail in website_details:
        link: str = website_detail.link
        if not any(word in link for word in FORBIDEN_WORDS):
            filtered_websites.append(website_detail)
    return filtered_websites