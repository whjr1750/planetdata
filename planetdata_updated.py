from selenium import webdriver
from selenium.webdriver.common.by import By #added this
from bs4 import BeautifulSoup
import time 
import csv
import requests

start_url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome("chromedriver.exe") #added this
browser.get(start_url)
time.sleep(10)
headers = ['name','light_years_from_earth','planet_mass','stellar_magnitude','discovery_date','hyperlink','planet_type','planet_radius',
'orbital_radius','orbital_radius','eccentricity']
planet_data = []
def scrap():
    
    for i in range(1,5):
        while True:
            soup = BeautifulSoup(browser.page_source,'html.parser')
            current_page_num = int(soup.find_all('input',attrs = {'class','page_num'})[0].get('value'))
            if current_page_num<i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num>i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all('ul',attrs = {'class','exoplanet'}):
            li_tags = ul_tag.find_all('li')
            temp_list = []
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append('')
            hyperlink_li_tag = li_tags[0] #made it li_tags instead of li_tag here
            temp_list.append('https://exoplanets.nasa.gov'+hyperlink_li_tag.find_all('a',href = True)[0]['href'])
            planet_data.append(temp_list)
            # browser.find_element_by_xpath('//*[@id = "primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() #added this and move indentation back
        print(f"Page {i} scraping completed")
    # with open('scraper.csv','w') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(headers)
    #     csv_writer.writerows(planet_data)
scrap()

new_planets_data = []

def scrap_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,'html.parser') 
        temp_list = []
        for tr_tag in soup.find_all('tr_tag',attrs = {'class':'fact_row'}):
            td_tags = tr_tag.find_all('td')
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all('div',attrs = {'class':'value'})[0].contents[0])
                except:
                    temp_list.append('')
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)
for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f'scraping at {index+1} is done')
print(new_planets_data[0:10])
final_planet_data = []
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planets_data[index]
    new_planet_data_element = [i.replace('\n','')for i in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)
with open('scraper.csv','w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(final_planet_data)



    


            

