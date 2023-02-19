import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Ask the user for input
year = input("Enter year: ")
card_set = input("Enter card set: ")
character = input("Choose character: ")
my_search = f"{year} {card_set} {character}"
print(my_search)

# Initialize the web driver
wd = webdriver.Chrome()

# Set an implicit wait time for the web driver
wd.implicitly_wait(10)

# Navigate to Amazon.com
wd.get("https://www.amazon.com/")

# Set the location to search results
wd.find_element(By.ID, "nav-global-location-popover-link").click()
postcode_field = wd.find_element(By.ID, "GLUXZipUpdateInput")
postcode_field.send_keys("91423")
wd.find_element(By.ID, "GLUXZipUpdate").click()
close_element = wd.find_element(By.CSS_SELECTOR, "button.a-button-text")
close_element.click()

# Search for the input
search_field = wd.find_element(By.NAME, "field-keywords")
search_field.send_keys(my_search)
search_button_click = wd.find_element(By.ID, "nav-search-submit-button")
search_button_click.click()

# Extract the search results with BeautifulSoup
soup = BeautifulSoup(wd.page_source, "html.parser")
web_page = soup.findAll("div", {"data-component-type": "s-search-result"})

# Create a list to store the search results
results_list = []

# Loop through the search results and extract the relevant data
for result in web_page:
    title = result.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
    price = result.find("span", {"class": "a-offscreen"})
    url = result.find("a", {"class": "a-link-normal s-no-outline"})
    character_match = result.find("span", text=re.compile(character, re.IGNORECASE))
    if title and price and url and character_match:
        title_text = title.text.strip()
        price_text = price.text.strip()
        url_text = "https://www.amazon.com" + url["href"]
        character_text = character_match.text.strip()
        print(f"{title_text} - {price_text} - {url_text} - {character_text}")
        results_list.append({"Title": title_text, "Price": price_text, "URL": url_text, "Character": character_text})

# Close the web driver
wd.quit()

# Convert the search results to a pandas DataFrame
df = pd.DataFrame(results_list)

# Drop rows without a price
df = df.dropna(subset=["Price"])

# Save the search results to a CSV file
df.to_csv("marvel_cards.csv", index=False)





