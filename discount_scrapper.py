from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
import undetected_chromedriver as uc
import timeit
from datetime import datetime


def main():

    #path = r"PATH"
    #driver = webdriver.Chrome(path)
    #driver.maximize_window()
    
    current_time = datetime.now().strftime("%Y.%m.%d %Hh%Mm") 
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://steamdb.info/sales/")
    driver.implicitly_wait(8)
    Select(driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_length']/label/select")).select_by_value("-1")
    driver.implicitly_wait(15)


    list_of_titles = []
    list_of_discounts = []
    list_of_prices = []
    timer_start = timeit.default_timer()   


    try:
        titles = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr/td[3]/a"))
                )
        list_of_titles += [title.text for title in titles]
        
        
        discounts = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr/td[4]"))
                )
        list_of_discounts += [discount.text for discount in discounts]
        
        
        prices = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr/td[5]"))
                )
        list_of_prices += [price.text for price in prices]
    
    
    except:
        print('terminated')
        driver.quit()
        
    
    result = pd.DataFrame(zip(list_of_titles, list_of_discounts, list_of_prices))
    result.columns = ["Title", "Discount", "Price"]
    result.to_csv(f"discounts/{str(current_time)} discounts.csv", index=False)
        
    
    timer_stop = timeit.default_timer()
    print("Runtime: ", timer_stop - timer_start, 's')
    
    
if __name__ == "__main__":
    main()