#Importing packages
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.select import Select
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import lxml
from IPython.display import display_html

def extractdse(fdate, tday, instrument):
    
    # load the driver, download chrome driver and put the .exe file in C:/Windows
    driver = webdriver.Chrome()

    # load DSE data archive site
    driver.get('https://www.dsebd.org/day_end_archive.php')
    
    # deal with the pop up warning
    try: 
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        print ("No alert here")
    
    # from date
    fdate=datetime.datetime.strptime(fdate, '%Y-%m-%d')
    yr=str(fdate.year)
    mn='0'+str(fdate.month)
    dy='0'+str(fdate.day)
    
    # to date
    tday=datetime.datetime.strptime(tday, '%Y-%m-%d')
    bdd='0'+str(tday.day)
    bdm='0'+str(tday.month)
    bdy=str(tday.year)
    
    # beginning day
    x=Select(driver.find_element_by_name("DayEndSumDate1_day"))
    x.select_by_value(dy)
    
    # beginning month
    y=Select(driver.find_element_by_name("DayEndSumDate1_month"))
    y.select_by_value(mn)

    # beginning year
    z=Select(driver.find_element_by_name("DayEndSumDate1_year"))
    z.select_by_value(yr)

    # end day
    xp=Select(driver.find_element_by_name("DayEndSumDate2_day"))
    xp.select_by_value(bdd)
    
    # end month
    yp=Select(driver.find_element_by_name("DayEndSumDate2_month"))
    yp.select_by_value(bdm)
    
    # end year
    zp=Select(driver.find_element_by_name("DayEndSumDate2_year"))
    zp.select_by_value(bdy)
    
    # instrument
    inst=Select(driver.find_element_by_name("Symbol"))
    inst.select_by_visible_text(instrument)
    
    # generate the table
    driver.find_element_by_name("ViewDayEndArchive").click()
    
    # extract the table
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tables = soup.find_all('table')
    tt=tables[374]
    k=pd.read_html(driver.page_source, header=0)[373]
    return(k)
    
extractdse('2019-01-01', '2019-03-03', 'ACI')
