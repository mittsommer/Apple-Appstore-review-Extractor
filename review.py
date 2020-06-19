# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import time
import pandas as pd
import splite


def seeting(url):
    # Setting up Chrome webdriver Options
    chrome_options = webdriver.ChromeOptions()
    # setting  up local path of chrome binary file
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    # creating Chrome webdriver instance with the set chrome_options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    return driver


def get_fullpage(driver):
    while True:
        driver.execute_script("window.scrollBy(0,3000)")
        time.sleep(1)
        i = 0
        if len(driver.find_elements_by_xpath("//div[@class='UD7Dzf']")) >= 5:
            break
        try:
            driver.find_elements_by_css_selector('.RveJvd')[0].click()
            i = i + 1
        except:
            continue



def get_review(driver):
    app_title = driver.find_element_by_class_name('AHFaub').text.replace(' ', '')
    app_title = app_title.replace(':', '')
    review = []
    for elem in driver.find_elements_by_xpath("//div[@class='UD7Dzf']"):
        content = elem.get_attribute('outerHTML')
        soup = BeautifulSoup(content, "html.parser")
        txt = soup.get_text()
        review.append(txt)
    return app_title, review


def save_csv(title, review):
    dataframe = pd.DataFrame({'review': review})
    dataframe.to_csv(title + '.csv', index=False, sep=',', encoding='utf_8_sig')


def main():
    url = ['https://play.google.com/store/apps/details?id=com.ubercab.eats&hl=ja&showAllReviews=true',
           'https://play.google.com/store/apps/details?id=com.demaecan.androidapp&hl=ja&showAllReviews=true',
           'https://play.google.com/store/apps/details?id=jp.co.rakuten.delivery&hl=ja&showAllReviews=true'
           ]
    for url in url:
        driver = seeting(url)
        get_fullpage(driver)
        app_title, review = get_review(driver)
        review_split = splite.splite(review)
        save_csv(app_title, review)
        save_csv(app_title + "split", review_split)



if __name__ == "__main__":
    # execute only if run as a script
    main()
