from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from pandas import *
masters_list = []


def extract_info(html_source):
    # html_source will be inner HTMl of table
    global lst
    soup = BeautifulSoup(html_source, 'html.parser')
    lst = soup.find('tbody').find_all('tr')
    for i in lst:
        cols = i.find_all('td')
        cols = [x.text.strip() for x in cols]
        masters_list.append(cols)

    # masters_list.append(lst)

    # i am printing just id because it's id set as crypto name you have to do more scraping to get more info


chrome_driver_path = '/Users/Justin/Desktop/Python/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver_path)
url = 'https://cryptoli.st/lists/fixed-supply'
driver.get(url)
loop = True

while loop:  # loop for extrcting all 120 pages
    crypto_table = driver.find_element(By.ID, 'DataTables_Table_0').get_attribute(
        'innerHTML')  # this is for crypto data table

    extract_info(crypto_table)

    paginate = driver.find_element(
        By.ID, "DataTables_Table_0_paginate")  # all table pagination
    pages_list = paginate.find_elements(By.TAG_NAME, 'li')
    # we clicking on next arrow sign at last not on 2,3,.. etc anchor link
    next_page_link = pages_list[-1].find_element(By.TAG_NAME, 'a')

    # checking is there next page available
    if "disabled" in next_page_link.get_attribute('class'):
        loop = False

    pages_list[-1].click()  # if there next page available then click on it

df = pd.DataFrame(masters_list)
print(df)
# df.to_csv("crypto_list.csv")
driver.quit()
