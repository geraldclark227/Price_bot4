import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import webbrowser


def search_cards():
    year = year_entry.get()
    card_set = card_set_entry.get()
    character = character_entry.get()

    driver = wd.Chrome(executable_path="C:\\Users\\q8mlg\\OneDrive\\Desktop\\driver\\chromedriver.exe")
    driver.implicitly_wait(10)

    df_amazon = search_amazon(driver, year, card_set, character)
    df_ebay = search_ebay(driver, year, card_set, character)

    driver.quit()

    df_combined = pd.concat([df_amazon, df_ebay], ignore_index=True)

    display_results(df_combined)


def search_amazon(driver, year, card_set, character):
    driver.get("http://www.amazon.com")
    my_search = f"{year} {card_set} {character}"

    search_field = driver.find_element(By.ID, "twotabsearchtextbox").send_keys(my_search)
    search_button_click = driver.find_element(By.ID, "nav-search-submit-button")
    search_button_click.click()
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    web_page = soup.findAll("div", {"data-component-type": "s-search-result"})

    row = ""
    result_list_1 = []

    for result in web_page:
        title = result.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        price = result.find("span", {"class": "a-offscreen"})
        url = result.find("a", {"class", "a-link-normal s-no-outline"})
        if title and price and url:
            row = [title.text,
                   price.text.replace("$", "").replace(",", ""),
                   "https://amazon.com/" + url['href']]
        result_list_1.append(row)

    # Dataframe Amazon
    df_a = pd.DataFrame.from_records(result_list_1, columns=["Title", "Price", "URL"])
    df_a["Title"] = df_a["Title"].str.strip()
    df_a_f1 = df_a[df_a["Title"].str.match(year)
                   & df_a["Title"].str.contains(card_set, case=False)
                   & df_a["Title"].str.contains(character, case=False)]
    df_a_f2 = df_a_f1.drop_duplicates(keep="first")

    # Save Amazon search results to CSV file
    df_a_f2.to_csv("amazon_cards.csv", index=False)

    return df_a_f2

def search_ebay(driver, year, card_set, character):
    driver.get("https://www.ebay.com/")
    my_search = f"{year} {card_set} {character}"

    search_field_ebay = driver.find_element(By.ID, "gh-ac").send_keys(my_search)
    search_button_ebay_click = driver.find_element(By.ID, "gh-btn")
    search_button_ebay_click.click()
    driver.implicitly_wait(10)

    soup_ebay = BeautifulSoup(driver.page_source, 'html.parser')
    web_page_ebay = soup_ebay.findAll("li", {"class": "s-item s-item__pl-on-bottom"})

    row_ebay = ""
    result_list_2 = []

    for result2 in web_page_ebay:
        title_ebay = result2.find("span", {"role": "heading"})
       
        price_ebay = result2.find("span", {"class": "s-item__price"})
        url_ebay = result2.find("a", {"class": "s-item__link"})
        if title_ebay and price_ebay and url_ebay:
            row_ebay = [title_ebay.text,
                        price_ebay.text.replace("$", "").replace(",", ""),
                        url_ebay['href']]
        result_list_2.append(row_ebay)

    # Dataframe eBay
    df_e = pd.DataFrame.from_records(result_list_2, columns=["Title", "Price", "URL"])
    df_e["Title"] = df_e["Title"].str.strip()
    df_e_f1 = df_e[df_e["Title"].str.match(year)
                   & df_e["Title"].str.contains(card_set, case=False)
                   & df_e["Title"].str.contains(character, case=False)]
    df_e_f2 = df_e_f1.drop_duplicates(keep="first")

    # Save eBay search results to CSV file
    df_e_f2.to_csv("ebay_cards.csv", index=False)

    return df_e_f2

def display_results(df):
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")

    tree = ttk.Treeview(results_window, columns=("Title", "Price", "URL"), show="headings")
    tree.column("Title", minwidth=0, width=300)
    tree.column("Price", minwidth=0, width=100)
    tree.column("URL", minwidth=0, width=300)

    tree.heading("Title", text="Title")
    tree.heading("Price", text="Price")
    tree.heading("URL", text="URL")

    for index, row in df.iterrows():
        tree.insert("", "end", values=(row["Title"], row["Price"], row["URL"]))

    tree.pack()

    save_button = ttk.Button(results_window, text="Save Results", command=lambda: save_results(df))
    save_button.pack()
import os

def open_url(event, tree):
    item = tree.item(tree.focus())['values']
    if item:
        url = item[2]
        webbrowser.open(url, new=1)


def display_results(df):
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")

    tree = ttk.Treeview(results_window, columns=("Title", "Price"), show="headings")
    tree.column("Title", minwidth=0, width=300)
    tree.column("Price", minwidth=0, width=100)

    tree.heading("Title", text="Title")
    tree.heading("Price", text="Price")

    for index, row in df.iterrows():
        tree.insert("", "end", values=(row["Title"], row["Price"], row["URL"]))

    tree.bind("<Double-1>", lambda event: open_url(event, tree))  # Bind the open_url function to a double-click event

    tree.pack()

    save_button = ttk.Button(results_window, text="Save Results", command=lambda: save_results(df))
    save_button.pack()



# GUI code
root = tk.Tk()
root.title("Marvel Card Search")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

year_label = ttk.Label(mainframe, text="Year:")
year_label.grid(column=1, row=1, sticky=tk.W)
year_entry = ttk.Entry(mainframe)
year_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

card_set_label = ttk.Label(mainframe, text="Card Set:")
card_set_label.grid(column=1, row=2, sticky=tk.W)
card_set_entry = ttk.Entry(mainframe)
card_set_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

character_label = ttk.Label(mainframe, text="Character:")
character_label.grid(column=1, row=3, sticky=tk.W)
character_entry = ttk.Entry(mainframe)
character_entry.grid(column=2, row=3, sticky=(tk.W, tk.E))

search_button = ttk.Button(mainframe, text="Search", command=search_cards)
search_button.grid(column=2, row=4, sticky=(tk.W, tk.E))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)
mainframe.rowconfigure(4, weight=1)

root.mainloop()
