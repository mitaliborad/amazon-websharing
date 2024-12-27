#import statements
from selenium import webdriver # open and controls web browser
from selenium.webdriver.common.keys import Keys # in output press enter , tab, backspace
from selenium.webdriver.common.by import By # for how to find element (by id, class, name)
from bs4 import BeautifulSoup #use for parsing HTML & XML
import time # for pause time
import pandas as pd #for data collect in csv
import os # import os module in python

data = [] # data for dictioonary


#  1. drive a amazon  and show 1 to 10 pages laptop data on amazon and show information of all laptop.
#Opens amazon's search results for the query "laptop."
driver = webdriver.Chrome()
query = "laptop"
file = 0

#Loops through the first 10  pages of search results.
for i in range(1,10):
    driver.get(f"https://www.amazon.in/s?k={query}&page=3&crid=2MW5PS1STZ96S&qid=1735275154&sprefix=%2Caps%2C265&ref=sr_pg_{i}")

    #Finds all elements matching the class name puis-card-container
    elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
    #Prints the number of items found on the page.
    print(f"{len(elems)} items found")
    print(elems)
    for elem in elems:
        #Saves the HTML content of each element to separate .html files in a folder named data.
        d = elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html","w", encoding="utf-8") as f:
            f.write(d)
            file +=1
        print(elem.text)
time.sleep(1)
driver.close()

#2. collect data from data folder and store title link and price in csv

for file in os.listdir("data") : # file in data folder
    try: # if in any file can't read link and title than ignore it

        with open (f"data/{file}") as f:# read every file in data folder
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser') 

        #find a tag with class which has link and title
        l = soup.find("a",class_="a-link-normal s-line-clamp-2 s-link-style a-text-normal", href=True)

        # find h2 for the title
        t = l.find("h2") 
        title = t.get_text()
        print("Title:", title)
        
        
        # find link 
        for link in l:
            link = "https://amazon.in/" + l['href']
            print("Link:", link)
            
        
        # find price in a-price-whole class in new attribute
        p = soup.find("span",attrs={"class" : 'a-price-whole'}) 
        price = (p.get_text()) 
        print("Price:", price)
        
        
        data.append({"Title": title, "Price": price, "Link": link})

    except Exception as e:
        print(e)


df = pd.DataFrame(data) # with the help of pandas create dataframe of  data 
df.to_csv("data.csv")  # convert df into csv file 


