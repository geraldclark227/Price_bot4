import pandas as pd
import numpy
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re

def run_web_driver(year1, card_set1, character1, psa_card1, my_search, beckett_url):
    from selenium import webdriver as wd
    from selenium.webdriver.common.by import By

    wd = wd.Chrome()
    wd.get(beckett_url)
    wd.implicitly_wait(10)
    try:
        beckett_compare_seller_btn = wd.find_element(By.CSS_SELECTOR,".btn.btn-success.compareItemsExpand")
        beckett_compare_seller_btn.click()
        wd.implicitly_wait(20)
    except:
        print("No button to select...")

    cookie_accept_btn = wd.find_element(By.CSS_SELECTOR,'.okBtn.acceptBtn')
    cookie_accept_btn.click()
    wd.implicitly_wait(30)

    beckett_soup = BeautifulSoup(wd.page_source,'html.parser')

    row_b=""
    result_list_b=[]
    outer = beckett_soup.find_all("ul")

    # Beckett Marketplace
    for s1 in outer:
        title3 = s1.find("li",{"class":"title"})
        price3 = s1.find("span", {"class":"item-price-value"})
        url3 =  s1.find("a", href=True)
        if title3 and price3 and url3:
            row_b = [title3.text, price3.text.replace("$","").replace(",",""),url3['href']]            
        result_list_b.append(row_b)
        #print(result_list_b)
            
    # Dataframe Beckett Marketplace
    df_b = pd.DataFrame.from_records(result_list_b, columns=["Title","Price","URL"])
    df_b["Title"] = df_b["Title"].str.strip()
    #print(df_b)
    df_b_f1 = df_b[df_b["Title"].str.contains(year1)
                    & df_b["Title"].str.contains(card_set1, case=False) 
                    & df_b["Title"].str.contains(character1, case=False)]
    df_b_f2 = df_b_f1.drop_duplicates(keep="first")
    df_b_f3 = df_b_f2[~df_b_f2["URL"].str.contains(pat='^javascript:void')]
    df_b_f4 = df_b_f3.sort_values(by="Price", ascending=False)
    print(df_b_f4)

    #amazon webdriver    
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

    soup = BeautifulSoup(wd.page_source,'html.parser')
    web_page = soup.findAll("div",{"data-component-type": "s-search-result"})

    row=""
    result_list_1=[]

    for result in web_page:
        title = result.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        price = result.find("span", {"class": "a-offscreen"}) 
        url = result.find("a", {"class", "a-link-normal s-no-outline"})
        if title and price and url:
            row = [title.text, price.text.replace("$","").replace(",",""), "https://amazon.com/" + url['href']]            
        result_list_1.append(row)
        
    # Dataframe Amazon
    df_a = pd.DataFrame.from_records(result_list_1, columns=["Title", "Price", "URL"])
    df_a["Title"] = df_a["Title"].str.strip()
    print(df_a)
    df_a_f1 = df_a[df_a["Title"].str.contains(year1)
                    & df_a["Title"].str.contains(pat='PSA', case=False)
                    & df_a["Title"].str.contains(psa_card1) 
                    & df_a["Title"].str.contains(card_set1, case=False) 
                    & df_a["Title"].str.contains(character1, case=False)]
    df_a_f2 = df_a_f1.drop_duplicates(keep="first")
    #df_a_f3 = df_a_f2.sort_values(by="Price", ascending=False)
    print(df_a_f2)

    # get ebay.com from webdriver
    wd.get("https://www.ebay.com/")
    wd.implicitly_wait(10)

    search_field_ebay = wd.find_element(By.ID, "gh-ac")
    search_field_ebay.send_keys(my_search)
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
            row_ebay = [title_ebay.text.replace("🔥", "").replace("💎","").replace("📈", "").replace("'",""),
                        price_ebay.text.replace("$","").replace(",",""),
                        url_ebay['href']]
        result_list_2.append(row_ebay)

    # Dataframe Ebay
    df_eb = pd.DataFrame.from_records(result_list_2, columns=["Title", "Price", "URL"])
    df_eb["Title"] = df_eb["Title"].str.strip()
    df_eb2 = df_eb[~df_eb["Price"].str.contains(pat="to", case=False)]
    df_eb_f1 = df_eb2[df_eb2["Title"].str.contains(year1)
                    & df_eb2["Title"].str.contains(pat='PSA', case=False)
                    & df_eb2["Title"].str.contains(psa_card1) 
                    & df_eb2["Title"].str.contains(card_set1, case=False) 
                    & df_eb2["Title"].str.contains(character1, case=False)]
    df_eb_f2 = df_eb_f1.drop_duplicates(keep="first")
    #df_eb_f3 = df_eb_f2.sort_values(by="Price", ascending=False)
    print(df_eb_f2)

    wd.close()

    #timestamp1 = datetime.datetime.now()
    c_list = [df_b_f4, df_a_f2, df_eb_f2]
    df_results_all = pd.concat(c_list, axis=0)
    df_results_all["Price"] = df_results_all["Price"].astype(float)
    df_results_all1 = df_results_all.sort_values(by="Price", ascending=False)
    df_results_all1.to_csv("marvel_cards.csv", index=False)
    print(df_results_all1)

    #excel writer with timestamp
    df_results_all1.to_excel("marvel_cards.xlsx")   

    wd.quit()

import webbrowser as wb
import tkinter as tk
import numpy
from tkinter import ttk, filedialog, messagebox

def open_link(event):
    #Opens the URL
    selected_row = tree_view.selection()
    try:
        row_url = tree_view.item(selected_row, "values")[2]
        #print(f"Going to {row_url}")
        wb.open_new_tab(row_url)
    except IndexError:
        print("Invalid row selected")

def column_style():
    tree_view.column("Title", width=600, anchor='w')
    tree_view.column("Price", minwidth=10, width=5, anchor='w')
    tree_view.column("URL", width=50, anchor='w')

    tree_view.heading("Title", anchor='w')
    tree_view.heading("Price", anchor='w')
    tree_view.heading("URL", anchor='w')

def open_excel():        
    my_excel1 = filedialog.askopenfilename(initialdir='\\Users\\geraldclark\\Desktop\\Price_bot4',
                                           title='Open excel',
                                           filetypes=(("Excel Files", "*.xlsx"),("All Files", "*.*")))
    if my_excel1:
        try:
            my_excel1 = r"{}".format(my_excel1)
            df_t_view = pd.read_excel(my_excel1)
            print(df_t_view)
        except Exception as e:
            messagebox.showerror("!", f'Must load excel spreadsheet...{e}')

    #remove unnamed column
    df_t_view2 = df_t_view.loc[:, ~df_t_view.columns.str.contains('^Unnamed')]

    #clear tree_view
    tree_view.delete(*tree_view.get_children())

    tree_view['column'] = list(df_t_view2.columns)
    tree_view['show'] = 'headings'

    for tree_col in tree_view['column']:
        tree_view.heading(tree_col, text=tree_col)  

    df_t_rows = df_t_view2.to_numpy().tolist()
    for r in df_t_rows:
        tree_view.insert("", "end", values=r)
    tree_view.bind('<Double-1>', open_link)

    column_style()

def submit():
    def column_style1():
        tree_view.column("Title", width=600, anchor='w')
        tree_view.column("Price", minwidth=10, width=5, anchor='w')
        tree_view.column("URL", width=50, anchor='w')

        tree_view.heading("Title", anchor='w')
        tree_view.heading("Price", anchor='w')
        tree_view.heading("URL", anchor='w')
    def auto_load_first_excel():
        dataframe_first_excel = pd.read_excel("marvel_cards.xlsx")
        dataframe_first_excel2 = dataframe_first_excel.loc[:, ~dataframe_first_excel.columns.str.contains('^Unnamed')]
        
        #clear tree_view
        tree_view.delete(*tree_view.get_children())

        tree_view['column'] = list(dataframe_first_excel2.columns)
        tree_view['show'] = 'headings'

        for tree_col in tree_view['column']:
            tree_view.heading(tree_col, text=tree_col)  

        df_t_rows2 = dataframe_first_excel2.to_numpy().tolist()
        for r2 in df_t_rows2:
            tree_view.insert("", "end", values=r2)
        tree_view.bind('<Double-1>', open_link)
        column_style1()


    #get variables from tkinter app
    year1 = year_var.get()
    card_set1 = card_set_var.get()
    character1 = character_var.get()
    psa_card1 = psa_card_var.get()

    split_cardset = card_set1.split()
    print(split_cardset)
    join_cardset = ("+".join(split_cardset))
    print(join_cardset)   

    my_search = f"{year1} {card_set1} {character1} PSA {psa_card1}"
    beckett_search = f"{year1}+{join_cardset}+{character1}"
    beckett_url=f"https://marketplace.beckett.com/search_new/?term={beckett_search}"
    print(beckett_search)

    run_web_driver(year1, card_set1, character1, psa_card1, my_search, beckett_url)

    auto_load_first_excel()

    print("year: " + year1)
    print("card set: " + card_set1)
    print("character: " + character1)
    print(psa_card1)
    print(type(psa_card1))
    
    #year_var.set("")
    #card_set_var.set("")
    #character_var.set("")
    #psa_card_var.set("10")

root = tk.Tk()
style = ttk.Style()
style.configure('Treeview.Heading', font=("Helvetica", 16))
style.configure('Treeview', font=("Helvetica", 14))
#style.configure("Treeview", rowheight=20, font="Helvetica", fontsize=20, background="white", foreground="black")

#root.tk.call("source", "forest-light.tcl")
#root.tk.call("source", "forest-dark.tcl")#
#style.theme_use("forest-dark")

root.title("Marvel Cards")
root.geometry("1500x400")
#root.pack_propagate(False)

year_var = tk.StringVar()
card_set_var = tk.StringVar()
character_var = tk.StringVar()
psa_card_var = tk.StringVar()

frame1 = tk.Frame(root, width=1500, height=400)
frame1.grid(row=0, column=0)

widgets_frame = tk.LabelFrame(frame1, text="Enter Data")
widgets_frame.place(relwidth=0.2, relheight=1.0, rely=0, relx=0.01)

frame_tree_view = tk.LabelFrame(frame1, text="Excel")
frame_tree_view.place(relwidth=0.75, relheight=1.0, rely=0, relx=0.21)

# Labels
yr_label = tk.Label(widgets_frame, text="Year")
yr_label.grid(row=0, column=0, padx=10, pady=5)
card_set_label = tk.Label(widgets_frame, text="Card Set")
card_set_label.grid(row=1, column=0, padx=10, pady=5)
character_label = tk.Label(widgets_frame, text="Character")
character_label.grid(row=2, column=0, padx=10, pady=5)
psa_label = tk.Label(widgets_frame, text="PSA")
psa_label.grid(row=3, column=0, padx=10, pady=5)

#year entry
yr_entry = tk.Entry(widgets_frame, textvariable = year_var, font=("Helvetica", 16))
yr_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#card set entry
c_set_entry = tk.Entry(widgets_frame, textvariable = card_set_var, font=("Helvetica", 16))
c_set_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

#character entry
character_entry = tk.Entry(widgets_frame, textvariable = character_var, font=("Helvetica", 16))
character_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

#PSA spin_box
psa_spinbox = tk.Spinbox(widgets_frame, textvariable=psa_card_var, from_=0, to=10, font=("Helvetica", 14))
psa_spinbox.grid(row=3, column=1, sticky="ew")

#scrollbar
v_scroll= ttk.Scrollbar(frame_tree_view)
#v_scroll.place(anchor='e')
v_scroll.pack(side ='right', fill ='y')

#treeview
tree_view = ttk.Treeview(frame_tree_view, show="headings", height=18)
tree_view.place(relheight=0.98, relwidth=0.98, rely=0, relx=0.01)
 
# Configuring scroll bar treeview
tree_view.configure(yscrollcommand = v_scroll.set)

#enter data
sub_btn = tk.Button(widgets_frame, text="Submit data", command=submit)
sub_btn.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

#open excel
excel_btn = tk.Button(widgets_frame, text="Open Excel File", command=open_excel)
excel_btn.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

#separator
separator = ttk.Separator(widgets_frame)
separator.grid(row=6, column=1, padx=10, pady=10, sticky="ew")


# #mode toggle, light and dark modes
# mode_switch = ttk.Checkbutton(
#         widgets_frame, text="Mode", style="Switch", command=toggle_mode)
# mode_switch.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

#tree_view.column(column="Title", width=150)

#column_style()
# scroll bar
# tree_scrolly = tk.Scrollbar(frame_tree_view, orient="vertical", command=tree_view.yview)
# tree_scrollx = tk.Scrollbar(frame_tree_view, orient="horizontal", command=tree_view.xview)
# tree_view.configure(xscrollcommand=tree_scrollx.set, yscrollcommand=tree_scrolly.set)
# tree_scrolly.place(rely=0, relx=0.90)
# tree_scrollx.place(rely=.90, relx=0)
#treescrollx.pack(side="bottom", fill="x")
#treescrolly.pack(side="right", fill="y")

root.mainloop()

#Marvel Masterpieces

