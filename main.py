from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import delay, writeToCsvRow





if __name__ == '__main__':
    #opening the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.delete_all_cookies()
    driver.set_window_size(1920, 1080)

    driver.get('https://www.google.ro/')
    driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div').click()
    searchBar = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    searchBar.send_keys('whatToScrap')
    searchBar.submit()
    delay()
