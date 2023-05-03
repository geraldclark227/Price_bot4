* Overview
   Our cards bot app help collectors and enthusiasts easily search and compare prices for Marvel trading cards across multiple online platforms,      including Beckett    Marketplace, Amazon, and eBay. The tool uses Python, web scraping, and the Tkinter library to create an efficient and user-friendly experience.

* Features
  -Search for Marvel trading cards based on the year, card set, character, and PSA grade
  -Scrape and extract relevant information, such as title, price, and URL, from search results on Beckett Marketplace, Amazon, and eBay
  -Store the extracted information in a DataFrame and export it to CSV and Excel files
  -Display the search results in a Tkinter GUI, allowing users to interact with the data and open product URLs directly from the application
   
* Dependencies
  - Python
  - Pandas
  - NumPy
  - Beautiful Soup
  - Selenium
  - Requests
  - Tkinter
   
* Usage
  -Input the desired search parameters, such as the year, card set, character, and PSA grade, into the Tkinter GUI.
  -Click the "Submit" button to begin the search.
  -The tool will scrape the search results from Beckett Marketplace, Amazon, and eBay, and store the extracted information in a DataFrame.
  -The DataFrame will be exported to a CSV and Excel file, and the search results will be displayed in the Tkinter GUI.
  -Users can interact with the data by double-clicking on a row in the search results to open the corresponding product URL in a web browser.
   
* Limitations
  -The tool is currently limited to searching for trading cards on Beckett Marketplace, Amazon, and eBay.
  -It may not work properly if the websites' structure or design changes, which may require updating the web scraping logic.
  -The tool is dependent on the availability of the websites being scraped and may not function if the websites are down or inaccessible.

* Third-party libraries used:
  - [Tkinter](https://docs.python.org/3/library/tkinter.html)
  - [Selenium](https://selenium-python.readthedocs.io/)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
  - [Pandas](https://pandas.pydata.org/)




