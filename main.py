from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests


import google
import utils
from google import search
from utils import delay

keys_to_search = 'CGS SERVICII FINANCIARE SRL'
google_response_class = "yuRUbf";

if __name__ == '__main__':
    #opening the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.delete_all_cookies()
    driver.set_window_size(1920, 1080)

    url = 'https://httpbin.org/ip'
    proxies = {
        "http": 'http://209.50.52.162:9050',
        "https": 'http://209.50.52.162:9050'
    }
    response = requests.get(url, proxies=proxies)
    print(response.json())
    # # search on google
    # search(driver, keys_to_search)
    #
    # # extract and filter responses
    # responses = driver.find_elements(By.CLASS_NAME, google_response_class)
    # website_details = google.web_element_to_website_details(responses)
    # filtered_websites = utils.filter_websites(website_details)



