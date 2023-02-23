import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from IPython.core.display import HTML

def search_amazon():
    # Get user input from GUI
    year = year_entry.get()
    card_set = card_set_entry.get()
    character = character_entry.get()
    postcode = postcode_entry.get()

    # Construct search string
    my_search = f"{year} {card_set} {character}"

    # Initialize the web driver
    wd = webdriver.Chrome()

    # Set an implicit wait time for the web driver
    wd.implicitly_wait(10)

    # Navigate to Amazon.com
    wd.get("https://www.amazon.com/")

    # Set the location to search results
    wd.find_element(By.ID, "nav-global-location-popover-link").click()
    postcode_field = wd.find_element(By.ID, "GLUXZipUpdateInput")
    postcode_field.send_keys(postcode)
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

    # Make URLs clickable in the dataframe
    df['URL'] = df['URL'].apply(lambda x: f'<a href="{x}">{x}</a>')
    HTML(df.to_html(escape=False))

    # Save the search results to a CSV file
    df.to_csv("amazon_cards.csv", index=False)

    # Show message box to confirm search results saved
    messagebox.showinfo("Amazon Search", "Search results saved to amazon_cards.csv")

# Create a function to display the CSV data in a new window
def show_results():
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv("amazon_cards.csv")

    # Create a new tkinter window to display the data
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")

    # Create a table to display the dataframe
    table = tk.Frame(results_window)
    table.pack()

    # Create a header row for the table
    header = df.columns
    for i in range(len(header)):
        label = tk.Label(table, text=header[i])
        label.grid(row=0, column=i)

    # Create a row for each result in the dataframe
    for i in range(len(df)):
        for j in range(len(header)):
            label = tk.Label(table, text=str(df[header[j]][i]))
            label.grid(row=i+1, column=j)

# Create GUI
root = tk.Tk()
root.title("Amazon Search")

# Create input fields and labels
year_label = tk.Label(root, text="Year:")
year_entry = tk.Entry(root)
card_set_label = tk.Label(root, text="Card Set:")
card_set_entry = tk.Entry(root)
character_label = tk.Label(root, text="Character:")
character_entry = tk.Entry(root)
postcode_label = tk.Label(root, text="Postcode:")
postcode_entry = tk.Entry(root)

# Create search button
search_button = tk.Button(root, text="Search", command=search_amazon)

# Create show results button
show_results_button = tk.Button(root, text="Show Results", command=show_results)

# Place input fields and labels in the grid
year_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
year_entry.grid(row=0, column=1, padx=5, pady=5)
card_set_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
card_set_entry.grid(row=1, column=1, padx=5, pady=5)
character_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
character_entry.grid(row=2, column=1, padx=5, pady=5)
postcode_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
postcode_entry.grid(row=3, column=1, padx=5, pady=5)

# Place search and show results buttons in the grid
search_button.grid(row=4, column=0, padx=5, pady=5, sticky="W")
show_results_button.grid(row=4, column=1, padx=5, pady=5, sticky="E")

# Start the GUI
root.mainloop()
