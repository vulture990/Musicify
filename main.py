from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
import pathlib
import os
from selenium.webdriver.common.by import By
import csv
to_csv = [
    {
        'debut date': 0,
        'peak date':0,
        'weeks on chart': 1,
        'wks40':0,
        'wks20':0,
        'wks10':0,
        'peakpos': 0,
        'weeks at peak':0,
        'rank':0,
        'artist': "",
        'title': ""
    }
]

driver = webdriver.Chrome(ChromeDriverManager().install())
keys = to_csv[0].keys()

pages = []

for file in sorted(os.listdir("input")):
    file_path = os.path.join(os.getcwd(),"input", file)
    file_uri = pathlib.Path(file_path).as_uri()
    pages.append(file_uri)



# so the way the algorithm is going to work is by looking in each billboard for new songs and each time it founds a new title it's going to save the debut date , peak date at first is going to be it's the date it's was new then if it got up we will update that date 
# we will also add a counter for number of weeks it stayed on chart
# and also a check for wks40 , wks20 and wks 10 
# then conclude the highest position it has ever been in
# weeks at peak how many weeks a title kept it's highest position  

result=[]

for i, page in enumerate(pages):
    driver.get(page)
    sleep(5)
    # get rows  
    rows = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, '.o-chart-results-list-row')
    except Exception as e:
        print("getting rows error:{}".format(e))
        # Get only the new titles (songs that are debuting) we are interested in getting more so the date
    for index, row in enumerate(rows):
            try:
                icondata = row.find_elements(By.CSS_SELECTOR, 'div')[3].get_attribute('innerHTML')
                continue
            except:
                icondata = 'new'
            try:
                peakpos =int(row.find_elements(By.CSS_SELECTOR, 'li span')[5].text.strip())
            except:
                peakpos = 0
            try:
                wks = int(row.find_elements(By.CSS_SELECTOR, 'li span')[6].text.strip()) 
            except:
                wks = 0
            title = row.find_element(By.CSS_SELECTOR, 'h3').text
            artist = row.find_elements(By.CSS_SELECTOR, 'li span')[3].text  
            position =  int(row.find_elements(By.CSS_SELECTOR, 'li span')[0].text.strip()) 
            wks40 = 0
            wks20 = 0
            wks10=0
            weeks_at_peak=0
            # rank how do you determine rank? : first song with most (highest peak) weeks on chart if not it's going to be the song with most weeks at peak if not it's going to be most with most weeks at 10 if not it's going to be most with most weeks at 20 if not it's going to be most with most weeks at 40 if not it's going to be the song with most weeks on chart
            rank=0
            date=page.split("_")[3]
            onedata = [position,date, peakpos, wks, artist, title]  
            result.append({
                'debut date': date,
                'peak date':date,
                'weeks on chart': 0,
                'wks40':wks40,
                'wks20':wks20,
                'wks10':wks10,
                'peakpos': peakpos,
                'weeks at peak':weeks_at_peak,
                'rank':rank,
                'artist': artist,
                'title': title
            })
            # save that into a unique csv file
            

            

            # result.append(onedata)
            # peak date is the day it peaked (date with highest position )
        
    # we got the new songs and their titles and artist and position and all that
    # now we will determine for each page their debuting date from the html we have in the input folder


# now that we have all debuting songs we need to process them so we can get the data we need 

    
# debut date is the day the song shows on the chart for the first time 
# peak date is the day it peaked (date with highest position )
# weeks on chart are the number of weeks on the charts
# wks40 is how many weeks a title has been on position between 1 -40
# wks 20 is how many weeks a title has been on position between 1 -20
# wks 10 is how many weeks a title has been on position between 1 -10
# peak position is the highest position a title has reached
# weeks at peak is how many weeks a title has been at its peak position and if peak position is 1 then how many week stays at 1
# rank how do you determine rank? : first song with most (highest peak) weeks on chart if not it's going to be the song with most weeks at peak if not it's going to be most with most weeks at 10 if not it's going to be most with most weeks at 20 if not it's going to be most with most weeks at 40 if not it's going to be the song with most weeks on chart
# i+1 is going to be the number of weeks
for i ,page in enumerate(pages):
    
    rows = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, '.o-chart-results-list-row')
    except Exception as e:
        print("getting rows error:{}".format(e))
    for index, row in enumerate(rows):
        tit=row.find_element(By.CSS_SELECTOR, 'h3').text
        for res in result:
            #if it found that new record then it's going to update the peak date and weeks on chart and wks40 and wks20 and wks10 and peak position and weeks at peak
            if res['title'] == tit:
                try:
                    res['peakpos'] = row.find_elements(By.CSS_SELECTOR, 'li span')[5].text.strip()
                except :
                    res['peakpos'] = 0
                try:
                    res['wks'] = int(row.find_elements(By.CSS_SELECTOR, 'li span')[6].text.strip())
                except:
                    res['wks'] = 0
                try:
                    res['position'] = int(row.find_elements(By.CSS_SELECTOR, 'li span')[0].text.strip())
                except:
                    res['position'] = 0
                # peak position is the highest position a title has reached
                if int(res['peakpos']) < int(res['position']):
                    res['peakpos'] = res['position']
                    # peak date is the date it peaked (date with highest position ) 
                    res['peak date'] = page.split("_")[3]
                # weeks at peak is how many weeks a title has been at its peak position and if peak position is 1 then how many week stays at 1
                else:
                    res['weeks at peak'] += 1
                if res['position'] <= 40:
                    res['wks40'] += 1
                if res['position'] <= 20:
                    res['wks20'] += 1
                if res['position'] <= 10:
                    res['wks10'] += 1
                res['weeks on chart']+=1
                break

# rank how do you determine rank? : first song with most (highest peak) weeks on chart if not it's going to be the song with most weeks at peak if not it's going to be most with most weeks at 10 if not it's going to be most with most weeks at 20 if not it's going to be most with most weeks at 40 if not it's going to be the song with most weeks on chart
for r in result:
    r['rank'] = 0
    for r2 in result:
        if int(r['peakpos']) < int(r2['peakpos']):
            r['rank'] += 1
        elif int(r['peakpos']) == int(r2['peakpos']):
            if int(r['weeks at peak']) < int(r2['weeks at peak']):
                r['rank'] += 1
            elif int(r['weeks at peak']) == int(r2['weeks at peak']):
                if r['wks10'] < r2['wks10']:
                    r['rank'] += 1
                elif int(r['wks10']) == int(r2['wks10']):
                    if r['wks20'] < r2['wks20']:
                        r['rank'] += 1
                    elif r['wks20'] == r2['wks20']:
                        if int(r['wks40']) < int(r2['wks40']):
                            r['rank'] += 1
                        elif r['wks40'] == r2['wks40']:
                            if int(r['weeks on chart'])< int(r2['weeks on chart']):
                                r['rank'] += 1
                            elif r['weeks on chart'] == r2['weeks on chart']:
                                pass
        
# now we have all the data we need and we can save it into a csv file

                
with open('output/new_songs.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)
    

