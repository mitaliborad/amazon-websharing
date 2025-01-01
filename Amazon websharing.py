#import statements
from selenium import webdriver # open and controls web browser
from selenium.webdriver.common.by import By # for how to find element (by id, class, name)
from selenium.webdriver.chrome.options import Options #for reduce detection
from bs4 import BeautifulSoup #use for parsing HTML & XML
from selenium.webdriver.support.ui import WebDriverWait # for waiting while all product elements appear on the page
from selenium.webdriver.support import expected_conditions as EC
import time # for pause time
import pandas as pd #for data collect in csv
import os # import os module in python

# Configure Chrome options to reduce detection
options = Options()
options.add_argument('disable-infobars') #removes the infobar at the top of the browser
options.add_experimental_option("excludeSwitches", ["enable-automation"]) # for reduce detection , enable automation
options.add_experimental_option('useAutomationExtension', False)#to turn off the Chrome automation extension

data = [] # data for dictioonary


#  1. drive a amazon  and show 1 to 10 pages laptop data on amazon and show information of all laptop.
#Opens amazon's search results for the query "laptop."
driver = webdriver.Chrome(options=options)
query = "laptop"
file = 0

#Loops through the first 10  pages of search results.
for i in range(0,11):
    url = f"https://www.amazon.in/s?k={query}&page={i}"
    driver.get(url)

    try:
        # Wait for products to load 5 untill find expected condition EC
        #presence_of_all_elements_located = expected condition used in conjunction with WebDriverWait
        #.s-main-slot = container holding all the products.
        #.s-result-item represents each individual product within that container.
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-main-slot .s-result-item"))
        )#web driver waits 10 seconds untill the our search result appear
        elems = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
        # all the search result items  that are located inside the main search results container 
        print(f"Page {i}: {len(elems)} items found")

        for elem in elems:
            try:
                d = elem.get_attribute("outerHTML") # Retrieves HTML structure for that product element.
                with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
                    f.write(d)
                print(f"Saved item {file}")
                file += 1
            except Exception as e:
                print(f"Error saving item {file}: {e}")
    except Exception as e:
        print(e)

time.sleep(4)
driver.close()


#2. collect data from data folder and store title link and price in csv

for file in os.listdir("data") : # file in data folder
    try: # if in any file can't read link and title than ignore it

        with open (f"data/{file}") as f:# read every file in data folder
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser') 

 #find a tag with class which has link and title
        # select-one = the first matching element.
        #.a-link-normal = class
        l = soup.select_one("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal[href]") 
 
        #using select-one CSS SELECTOR find title
        title = l.select_one("h2").get_text() 
        print("Title:", title)

        #link
        link = "https://amazon.in" + l["href"]
        print("Link:", link)
            
        
        # using select-one CSS SELECTOR find price
        p = soup.select_one("span.a-price-whole")
        price = p.get_text() 
        print("Price:", price)
        
        
        data.append({"Title": title, "Price": price, "Link": link})#data collection

    except Exception as e:
        print(e)


df = pd.DataFrame(data) # with the help of pandas create dataframe of  data 
df.to_csv("data.csv")  # convert df into csv file 