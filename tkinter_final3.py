import pandas as pd
import numpy
from datetime import datetime
from bs4 import BeautifulSoup

def run_web_driver(year1, card_set1, character1, psa_card1, my_search):
    #import pandas as pd
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
            row = [title.text, price.text.replace("$","").replace(",",""), "https://amazon.com/" + url['href']]            
        result_list_1.append(row)
        #print(result_list_1)
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
            row_ebay = [title_ebay.text.replace("🔥", "").replace("💎","").replace("'",""),
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
    df_results_all = pd.concat([df_a_f2, df_eb_f2], axis=0)
    df_results_all["Price"] = df_results_all["Price"].astype(float)
    df_results_all1 = df_results_all.sort_values(by="Price", ascending=False)
    df_results_all1.to_csv("marvel_cards.csv", index=False)
    print(df_results_all1)

    #excel writer with timestamp
    #writer1 = pd.ExcelWriter('excel_files\marvel_cards_{}.xlsx'.format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S")))
    df_results_all1.to_excel("marvel_cards.xlsx")   

    wd.quit()

import webbrowser as wb
import tkinter as tk
import customtkinter
import numpy
from tkinter import ttk, filedialog, messagebox
from IPython.display import HTML

# def toggle_mode():
#     if mode_switch.instate(["selected"]):
#         style.theme_use("forest-light")
#     else:
#         style.theme_use("forest-dark")

customtkinter.set_appearance_mode("Light")

def submit():
    #global year1
    year1 = year_var.get()
    #global card_set1
    card_set1 = card_set_var.get()
    #global character1
    character1 = character_var.get()
    #global psa_card1
    psa_card1 = psa_card_var.get()
   
    #global my_search
    #my_search = str(year1)+" "+str(card_set1)+" "+str(character1)
    my_search = f"{year1} {card_set1} {character1} PSA {psa_card1}"

    run_web_driver(year1, card_set1, character1, psa_card1, my_search)

    print("year: " + year1)
    print("card set: " + card_set1)
    print("character: " + character1)
    print(psa_card1)
    print(type(psa_card1))
    
    #year_var.set("")
    #card_set_var.set("")
    #character_var.set("")
    psa_card_var.set("10")

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
    tree_view.column("Title", width=500, anchor='w')
    tree_view.column("Price", minwidth=10, width=5, anchor='w')
    tree_view.column("URL", width=50, anchor='w')

    tree_view.heading("Title", anchor='w')
    tree_view.heading("Price", anchor='w')
    tree_view.heading("URL", anchor='w')

def clear_tree_view():
    tree_view.delete(*tree_view.get_children())

def open_excel():
    #filetypes = ("Excel Files", ".xlsx"),("All Files", "*.*")
    my_excel1 = filedialog.askopenfilename(title='Open excel', 
                                           initialdir='/Users/geraldclark/Desktop/Price_bot4', 
                                           filetypes=(("Excel Files", ".xlsx"),("All Files", "*.*")))
    
    try:
        df_t_view = pd.read_excel(my_excel1)
        print(df_t_view)
    except Exception as e:
        messagebox.showerror("!", f"Must load excel spreadsheet...{e}")

    #remove unnamed column yup
    df_t_view2 = df_t_view.loc[:, ~df_t_view.columns.str.contains('^Unnamed')]

    clear_tree_view()

    tree_view['column'] = list(df_t_view2.columns)
    tree_view['show'] = 'headings'

    for tree_col in tree_view['column']:
        tree_view.heading(tree_col, text=tree_col)  

    df_t_rows = df_t_view2.to_numpy().tolist()
    for r in df_t_rows:
        tree_view.insert("", "end", values=r)
    tree_view.bind('<Double-1>', open_link)

    column_style()

root = customtkinter.CTk()
style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 16))
#style.configure('Treeview', font=("Helvetica", 14))
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

frame1 = customtkinter.CTkFrame(root, width=1500, height=400)
frame1.grid(row=0, column=0)

widgets_frame = ttk.LabelFrame(frame1, text="Enter Data")
widgets_frame.place(relwidth=0.2, relheight=1.0)

frame_tree_view = ttk.LabelFrame(frame1, text="Tree View Excel")
frame_tree_view.place(relwidth=0.75, relheight=1.0, rely=0, relx=0.21)

# Labels
yr_label = customtkinter.CTkLabel(widgets_frame, text="Year")
yr_label.grid(row=0, column=0, padx=10, pady=5)
card_set_label = customtkinter.CTkLabel(widgets_frame, text="Card Set")
card_set_label.grid(row=1, column=0, padx=10, pady=5)
character_label = customtkinter.CTkLabel(widgets_frame, text="Character")
character_label.grid(row=2, column=0, padx=10, pady=5)
psa_label = customtkinter.CTkLabel(widgets_frame, text="PSA")
psa_label.grid(row=3, column=0, padx=10, pady=5)

#year entry
yr_entry = ttk.Entry(widgets_frame, textvariable = year_var, font=("Helvetica", 16))
yr_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#card set entry
c_set_entry = ttk.Entry(widgets_frame, text="", textvariable = card_set_var, font=("Helvetica", 16))
c_set_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

#character entry
character_entry = ttk.Entry(widgets_frame, textvariable = character_var, font=("Helvetica", 16))
character_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

#PSA spin_box
psa_spinbox = ttk.Spinbox(widgets_frame, textvariable=psa_card_var, from_=0, to=10, font=("Helvetica", 14))
psa_spinbox.grid(row=3, column=1, sticky="ew")

#treeview
tree_view = ttk.Treeview(frame_tree_view, show="headings", height=18)
tree_view.place(relheight=0.9, relwidth=0.9)

#enter data
sub_btn = customtkinter.CTkButton(widgets_frame, text="Submit data", command=submit)
sub_btn.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

#open excel
excel_btn = customtkinter.CTkButton(widgets_frame, text="Open Excel File", command=open_excel)
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

