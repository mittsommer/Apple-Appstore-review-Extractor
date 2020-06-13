#load webdriver function from selenium
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import time
import pandas as pd

def seeting():
    #Setting up Chrome webdriver Options
    chrome_options = webdriver.ChromeOptions()
    #setting  up local path of chrome binary file
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #creating Chrome webdriver instance with the set chrome_options
    driver = webdriver.Chrome(options=chrome_options)
    link = "https://play.google.com/store/apps/details?id=com.demaecan.androidapp&hl=ja&showAllReviews=true"
    driver.get(link)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    Ptitle = driver.find_element_by_class_name('AHFaub').text.replace(' ','')
    print(Ptitle)
    return driver

def get_fullpage(driver):
    while True:
        driver.execute_script("window.scrollBy(0,3000)")
        time.sleep(1)
        i = 0
        try:
            driver.find_elements_by_css_selector('.RveJvd')[0].click()
            i = i + 1
        except:
            continue
        if len(driver.find_elements_by_xpath("//div[@class='UD7Dzf']")) >= 500:
            break
reviews_df = set()

def get_review(driver):
    i = 0
    for elem in driver.find_elements_by_xpath("//div[@class='UD7Dzf']"):
        content = elem.get_attribute('outerHTML')
        soup = BeautifulSoup(content, "html.parser")
        txt = soup.get_text()
        i=i+1
        print(i,txt)


def main():
    driver = seeting()
    get_fullpage(driver)
    get_review(driver)


if __name__ == "__main__":
    # execute only if run as a script
    main()