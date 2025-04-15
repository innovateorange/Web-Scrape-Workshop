import pandas as pd
import requests 
from bs4 import BeautifulSoup

#og link is https://www.scrapethissite.com/pages/forms/
headers = {
    "User-Agent" :  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

results = []
count = 0

#in this case there are different pages on the table, 1-24, so we are going to go through each one
for pagenum in range(1, 25):
    #we go the link with the modified page num
    link = f"https://www.scrapethissite.com/pages/forms/?page_num={pagenum}"
    response = requests.get(link, headers=headers)

    #if we are good, continue, else print error
    if response.status_code == 200:


        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all('tr', class_='team')

        for info in data:

            #go through each data piece in the table, use cooresponding class names
            #use text.strip() to clean up data -- otherwise we have alot of spaces
            name = info.find('td', class_='name').text.strip()
            
            year = info.find('td', class_='year').text.strip()

            wins = info.find('td', class_='wins').text.strip()
    
            losses = info.find('td', class_='year').text.strip()

            overtime_losses= info.find('td', class_='ot-losses').text.strip()


            
            win_percentage = info.find('td', class_='pct text-success')
            #test case for win percentage because there are two different cases
            #one where the win pct is red and one where it is green (denoted by danger and success in the tag)
            if not win_percentage:
                win_percentage = info.find('td', class_='pct text-danger').text.strip()
            else: 
                win_percentage = win_percentage.text.strip()

            
            goals_for = info.find('td', class_='gf').text.strip()

            goals_against = info.find('td', class_='ga').text.strip()

            goal_differential = info.find('td', class_='diff text-success')
            #again this is a case where it can have two different names so we check the other if one doesn't exist
            if not goal_differential:
                goal_differential = info.find('td', class_='diff text-danger').text.strip()
            else:
                goal_differential = goal_differential.text.strip()

            #append all the data to our results
            results.append({
            "Name": name,
            "Year" : year,
            "Wins" : wins,
            "Losses" : losses,
            "OT losses" : overtime_losses,
            "Goals For (GF)" : goals_for,
            "Goals Against (GA)" : goals_against,
            "Goal Differential" : goal_differential
            })

    #if we didn't load the page tell us error and the page num it failed on 
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Page number : {pagenum}")
            

    
#saving the data to a dataframe
df = pd.DataFrame(results)
#print(df.head())

#saving it to a csv
df.to_csv("HockeyTeams.csv")
print("Data saved to HockeyTeams.csv")
    


    




