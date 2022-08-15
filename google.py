from selenium.webdriver.common.by import By


class WebsiteDetails:
    def __init__(self, link, desc):
        self.link = link
        self.description = desc

    def __str__(self) -> str:
        return 'link -> ' + self.link + ' \ndescription -> ' + self.description + '\n'


def search(driver, keys_to_search: str):
    driver.get('https://www.google.ro/')
    try:
        driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div').click()
    except:
        pass
    searchBar = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    searchBar.send_keys(keys_to_search)
    searchBar.submit()


def web_element_to_website_details(responses):
    website_details = []
    for response in responses:
        arr = response.text.split('\n')
        try:
            description = arr[1] + arr[0]
        except:
            description = 'No description'
        link = response.find_element(By.TAG_NAME, 'a').get_attribute('href')
        website_details.append(WebsiteDetails(link, description))
    return website_details
