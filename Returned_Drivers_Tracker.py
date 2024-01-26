from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
from datetime import date
import pandas as pd
import googlemaps


options = Options()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                        options = options)
columns = {'RouteCode':str,'DA Name':str,'LastStopAddress':str,'LastStopTime':str,'App login Time':str,
           'Planned End Time':str,'DistanceLastStopToDA':str,'TravelTimeLastStopToDA':str,'LastStopAddress':str}
df = pd.DataFrame(columns=columns.keys()).astype(columns)
pd.set_option('display.max_columns', None)

def getGoogleMapsData(origin,destination,mode='driving'):
    gmaps = googlemaps.Client(key='')
    directions_result=gmaps.directions(origin,destination,mode=mode)
    if directions_result:
        total_distance=directions_result[0]['legs'][0]['distance']['text']
        total_duration=directions_result[0]['legs'][0]['duration']['text']
    return [total_distance,total_duration]

def loginWebsiteOne(company_name):
    company_dict={'company 1':'alkdsjf','company 2':'oweiur','company 3':'company','company 4':'zoiudhs'}
    try:
        company_id = company_dict[str(company_name).lower()]
    except KeyError:
        print(f"Error: Company Name '{company_id}' not found in the dictionary.")
        exit
    today = date.today().strftime("%Y/%m/%d")
    year = today.split('/')[0].strip()
    month = today.split('/')[1].strip()
    day = int(today.split('/')[2].strip())
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    exampleUrl = f"https://EXAMPLE.com/{year}-{month}-{day}-{company_id}"
    driver.get(exampleUrl)
    username = driver.find_element('xpath','//*[@EXAMPLE_TAG = ""]')
    username.send_keys('')
    pin = driver.find_element('xpath','//*[@EXAMPLE_TAG = "password"]')
    pin.send_keys('')
    submit = driver.find_element('xpath','//*[@EXAMPLE_TAG="submit"]')
    submit.click()
    driver.implicitly_wait(30)
    time.sleep(2)

def websiteLoop(driverToHelp):
    da_list = driver.find_elements('xpath',"//a[@EXAMPLE_TAG='']")
    len_da_list = len(da_list)
    if len_da_list>0:
        for x in range(len_da_list-1):
            route_code = driver.find_element('xpath',f"//div[@EXAMPLE_TAG='']/div[{x+2}]/a[@EXAMPLE_TAG='']/div/div/div/div/div[2]").text
            da_name = driver.find_element('xpath',f"//div[@EXAMPLE_TAG='']/div[{x+2}]/a[@EXAMPLE_TAG=' ']/div/div/div/div/div/p[1]/span").text
            da_element = driver.find_element('xpath',f"//div[a[@EXAMPLE_TAG='']][{x+1}]")
            da_element.click()
            backbutton = driver.find_element('xpath','//*[]')
            time.sleep(1)
            try:
                delivered_stops_list = driver.find_elements('xpath',"//a[@EXAMPLE_TAG='']//p[contains(text(),'')]/parent::div/p/span[@EXAMPLE_TAG='']")
                if len(delivered_stops_list)>0:
                    last_delivered_stop = driver.find_element('xpath',f"//a[@EXAMPLE_TAG=' '][div//p[contains(text(), '')]][{len(delivered_stops_list)}]//p/span[@EXAMPLE_TAG='']")
                    last_delivered_stop.click()
                    last_delivered_stop_address = driver.find_element('xpath',"//p[@EXAMPLE_TAG='' and not(contains(text(),'')) and not(contains(text(),''))]").text
                    last_delivered_stop_time = driver.find_element('xpath',"//p[]").text
                    googlemapsData = getGoogleMapsData(origin=last_delivered_stop_address,destination='')
                    DistanceLastStopToDA = googlemapsData[0]
                    TravelTimeLastStopToDA = googlemapsData[1]
                    backbutton.click()
                    planned_endtime = driver.find_element('xpath',"//p[EXAMPLE_TAG(text())='']/following-sibling::p[]").text
                    login_time = driver.find_element('xpath',"//p[EXAMPLE_TAG(text())='']/following-sibling::p[]").text
                    df.loc[len(df.index)] = [route_code,da_name,last_delivered_stop_address,last_delivered_stop_time,login_time,planned_endtime,DistanceLastStopToDA,str(TravelTimeLastStopToDA),'']
            except NoSuchElementException:
                df.loc[len(df.index)] = [route_code,da_name,'','',login_time,planned_endtime,'','','']
            except StaleElementReferenceException:
                df.loc[len(df.index)] = [route_code,da_name,'','',login_time,planned_endtime,'','','']
            backbutton.click()
            time.sleep(3)
    else:
        print('NO DRIVERS FOUND')

loginWebsiteOne(company='COMPANY 1') 
websiteLoop(driverToHelp='JOHN DOE',)
df.sort_values(by='TravelTimeLastStopToDA',ascending=True)
df.to_excel('FILENAME.xlsx',index=False)