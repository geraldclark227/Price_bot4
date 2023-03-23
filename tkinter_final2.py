import pandas as pd
from bs4 import BeautifulSoup

def run_web_driver():
    from selenium import webdriver as wd
    from selenium.webdriver.common.by import By
    
    wd = wd.Chrome()
    wd.get("http://www.amazon.com")
    wd.implicitly_wait(10)

    #__zip code for locality of order__
    #wd.find_element(By.ID,"nav-global-location-popover-link").click()
    #postcode_field = wd.find_element(By.ID,"GLUXZipUpdateInput")
    #postcode_field.send_keys("91423")
    #wd.find_element(By.ID,"GLUXZipUpdate").click() 
    #close_element = wd.find_element(By.CSS_SELECTOR, "button.a-button-text")
    #close_element.click()
    #wd.implicitly_wait(10)
        
    #search_field = wd.find_element(By.ID, "twotabsearchtextbox").send_keys(my_search)
    search_field = wd.find_element(By.ID, "twotabsearchtextbox")
    search_field.send_keys(my_search)
    search_button_click = wd.find_element(By.ID, "nav-search-submit-button")
    search_button_click.click()
    wd.implicitly_wait(10)

    soup = BeautifulSoup(wd.page_source, 'html.parser')
    web_page = soup.findAll("div",{"data-component-type": "s-search-result"})

    row=""
    result_list_1=[]

    for result in web_page:
        title = result.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        price = result.find("span", {"class": "a-offscreen"}) 
        url = result.find("a", {"class", "a-link-normal s-no-outline"})
        if title and price and url:
            row = [title.text, 
                price.text.replace("$","").replace(",",""), 
                "https://amazon.com/" + url['href']]            
        result_list_1.append(row)
    # Dataframe Amazon
    df_a = pd.DataFrame.from_records(result_list_1, columns=["Title", "Price", "URL"])
    df_a["Title"] = df_a["Title"].str.strip()
    #df_a["Price"] = df_a["Price"].astype(float)
    df_a_f1 = df_a[df_a["Title"].str.match(year1) 
        & df_a["Title"].str.contains(card_set1, case=False) 
        & df_a["Title"].str.contains(character1, case=False)]
    df_a_f2 = df_a_f1.drop_duplicates(keep="first")
    #df_a_f3 = df_a_f2.sort_values(by="Price", ascending=False)
    print(df_a_f2)

    # get ebay.com from webdriver
    wd.get("https://www.ebay.com/")
    wd.implicitly_wait(10)

    search_field_ebay = wd.find_element(By.ID, "gh-ac").send_keys(my_search)
    search_button_ebay_click = wd.find_element(By.ID, "gh-btn")
    search_button_ebay_click.click()
    wd.implicitly_wait(10)

    soup_ebay = BeautifulSoup(wd.page_source, 'html.parser')
    web_page_ebay = soup_ebay.findAll("li",{"class": "s-item s-item__pl-on-bottom"})

    row_ebay=""
    result_list_2=[]

    for result2 in web_page_ebay:
        title_ebay = result2.find("span",{"role": "heading"})
        price_ebay = result2.find("span",{"class": "s-item__price"})
        #seller_rating = result2.find("span", {"class": "s-item__seller-info-text"})
        url_ebay = result2.find("a", {"class": "s-item__link"})
        if title_ebay and price_ebay and url_ebay:
            row_ebay = [title_ebay.text.replace("🔥", "").replace("💎","").replace("'",""),
                        price_ebay.text.replace("$","").replace(",",""),
                        url_ebay['href']]
        result_list_2.append(row_ebay)

    # Dataframe Ebay
    df_eb = pd.DataFrame.from_records(result_list_2, columns=["Title", "Price", "URL"])
    df_eb["Title"] = df_eb["Title"].str.strip()
    df_eb2 = df_eb[~df_eb["Price"].str.contains("to", case=False)]
    #df_eb2["Price"] = df_eb2["Price"].astype(float)
    df_eb_f1 = df_eb2[df_eb2["Title"].str.contains(year1) 
        & df_eb2["Title"].str.contains(card_set1, case=False) 
        & df_eb2["Title"].str.contains(character1, case=False)]
    df_eb_f2 = df_eb_f1.drop_duplicates(keep="first")
    #df_eb_f3 = df_eb_f2.sort_values(by="Price", ascending=False)
    print(df_eb_f2)

    #webdriver close
    #wd.quit()
    wd.close()

    df_results_all = pd.concat([df_a_f2, df_eb_f2], axis=0)
    df_results_all["Price"] = df_results_all["Price"].astype(float)
    df_results_all1 = df_results_all.sort_values(by="Price", ascending=False)
    df_results_all1.to_csv("marvel_cards.csv", index=False)
    df_results_all1.to_excel("marvel_cards.xlsx")
    print(df_results_all1)

    wd.quit()


import tkinter as tk
import customtkinter
import numpy
from tkinter import ttk, filedialog

#def open_excel():
    #my_file1 = 


root = tk.Tk()
root.geometry("850x400")
root.title("Marvel Cards")
root.pack_propagate(False)

year_var = tk.StringVar()
card_set_var = tk.StringVar()
character_var = tk.StringVar()


def submit():
    global year1
    year1 = year_var.get()
    global card_set1
    card_set1 = card_set_var.get()
    global character1
    character1 = character_var.get()
    global my_search
    #my_search = str(year1)+" "+str(card_set1)+" "+str(character1)
    my_search = f"{year1} {card_set1} {character1}"

    print("year: " + year1)
    print("card set: " + card_set1)
    print("character: " + character1)
    
    year_var.set("")
    card_set_var.set("")
    character_var.set("")

yr_label = tk.Label(root, text="year", font=("Helvetica", 18, "normal"))
yr_entry = tk.Entry(root, textvariable = year_var, font=("Helvetica", 18, "normal"), width = 35)
#yr_entry.focus_set()
c_set_label = tk.Label(root, text="card set", font=("Helvetica", 18, "normal"))
c_set_entry = tk.Entry(root, textvariable = card_set_var, font=("Helvetica", 18, "normal"), width = 35)

character_label = tk.Label(root, text="character", font=("Helvetica", 18, "normal"))
character_entry = tk.Entry(root, textvariable = character_var, font=("Helvetica", 18, "normal"), width = 35)

sub_btn = tk.Button(root, text="Submit", command = submit)
run_web_driver_btn = tk.Button(root, text="Run Webdriver", command = run_web_driver)

yr_label.grid(row=0, column=0, padx=5, pady=5)
yr_entry.grid(row=0, column=1, padx=5, pady=5)
c_set_label.grid(row=1, column=0, padx=5, pady=5)
c_set_entry.grid(row=1, column=1, padx=5, pady=5)
character_label.grid(row=3, column=0, padx=5, pady=5)
character_entry.grid(row=3, column=1, padx=5, pady=5)
sub_btn.grid(row=4, column=1, padx=5, pady=5)
run_web_driver_btn.grid(row=5, column=1, padx=5, pady=5)

#tkinter mainloop
root.mainloop()
