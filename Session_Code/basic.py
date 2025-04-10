import pandas as pd
import requests 
from bs4 import BeautifulSoup

link = "https://www.scrapethissite.com/pages/simple/"

headers = {
    "User-Agent" :  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


#this gets the data from the your link, using the agent we created in header
response = requests.get(link, headers=headers)

#if it does respond, we good
if response.status_code == 200:

    #this gets our data into one varaible, basically grabs the html data
    soup = BeautifulSoup(response.text, "html.parser")

    #finds all the information under col-md-4 country 
    #since this is the class that holds the information we want
    #you can look further at htlm of website 
    data = soup.find_all('div', class_='col-md-4 country')
    
    #make a list to keep our data
    results = []

    #looking for the the country info inisde our data
    for info in data:

        #going through the different classes to get the information we want
        #again, look through html to see class names. 
        #text.strip gets the data nicely
        name = info.find('h3', class_='country-name').text.strip()

        capital = info.find('span', class_='country-capital').text.strip()

        population = info.find('span', class_='country-population').text.strip()

        area = info.find('span', class_='country-area').text.strip()


        #append this country's information to our results
        results.append({
            "Name": name,
            "Capital" : capital,
            "Population" : population,
            "Size" : area
        })
        
    #saving as a data frame
    df = pd.DataFrame(results)
    print(df.head())


    #save it to a csv file so you can do something with it
    df.to_csv("countries.csv", index=False)
    print("Data saved to 'countries.csv'")


    



#if it can't fetch data, print that it failed and tell you the status code
else: print(f"Failed to fetch data. Status code: {response.status_code}")
