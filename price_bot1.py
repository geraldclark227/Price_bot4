import re
from selenium import webdriver as wd
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
import time
#from selenium.webdriver.support import expected_conditions as EC

#PATH = '/Users/geraldclark/Downloads/chromedriver_mac_arm64'
wd = wd.Chrome()
wd.get("http://www.amazon.com")

#locality for order
#wd.find_element(By.ID,"nav-global-location-popover-link").click()
#postcode_field = wd.find_element(By.ID,"GLUXZipUpdateInput")
#postcode_field.send_keys("91423")
#wd.find_element(By.ID,"GLUXZipUpdate").click() 
#close_element = wd.find_element(By.CSS_SELECTOR, "button.a-button-text")
#close_element.click()
wd.implicitly_wait(10)

year = input("enter year: ")
year = str(year)

card_set = input("card_set: ")
card_set = str(card_set)

character = input("Choose character: ")
character = str(character)
my_search = f"{year} {card_set} {character}"
#print(my_search)

search_field = wd.find_element(By.NAME, "field-keywords").send_keys(my_search)
search_button_click = wd.find_element(By.ID, "nav-search-submit-button")
search_button_click.click()
wd.implicitly_wait(10)

import pandas as pd
from bs4 import BeautifulSoup

soup = BeautifulSoup(wd.page_source, 'html.parser')
web_page = soup.findAll("div",{"data-component-type": "s-search-result"})

row = ""
result_list=[]

#df_all_results = pd.DataFrame(columns=["Title", "Price", "Character", "URL"])

for result in web_page:
    title = result.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
    price = result.find("span", {"class": "a-offscreen"}) 
    url = result.find("a", {"class", "a-link-normal s-no-outline"})
    if title and price and url:
        row = [ title.text, price.text, "https://amazon.com/" + url['href']]
    result_list.append(row)

df_all_results = pd.DataFrame.from_records(result_list, columns=["Title", "Price", "URL"])
df_filtered = df_all_results.drop_duplicates(keep="first")
df_filtered2 = df_filtered[~df_filtered["Title"].str.contains("Set|Complete|Gift|Box|Comic Book|Comic|Pack|Action Figure|Figure|T-Shirt|Lego", re.IGNORECASE)]

wd.quit()

print(df_filtered2)
df_filtered2.to_csv("marvel_cards.csv", index=False)
df_filtered2.to_excel("marvel_cards.xlsx")


# You must install-->
# pip install openpyxl
# pip install importlib_metadata
# pip install chromedriver-py==110.0.5481.77
# pip install selenium
# uninstall chromedriver from mac, "brew uninstall --cask chromedriver"
# pip install beautifulsoup4
# Marvel Masterpieces
