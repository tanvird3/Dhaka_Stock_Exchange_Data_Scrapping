def extractdse(fdate, tday, instrument):
    
    #Importing packages
    import pandas as pd, datetime, lxml
    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    from bs4 import BeautifulSoup
    from IPython.display import display_html
    
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
    fd=fdate
    fdate=datetime.datetime.strptime(fdate, '%Y-%m-%d')
    yr=str(fdate.year)
    mn='0'+str(fdate.month)[-2:]
    dy='0'+str(fdate.day)[-2:]
    
    # to date
    td=tday
    tday=datetime.datetime.strptime(tday, '%Y-%m-%d')
    bdd='0'+str(tday.day)[-2:]
    bdm='0'+str(tday.month)[-2:]
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
    k=pd.read_html(driver.page_source, header=0)[len(tables)-5]
    k=k.drop(['#'], axis=1)
    
    # write the file to xlsx
    fn=instrument+'-'+fd+'-'+'to'+'-'+td+'.xlsx'
    k.to_excel(fn, index=False)
    
    return(k)
    
extractdse('2019-01-01', '2019-03-03', 'ACI')
