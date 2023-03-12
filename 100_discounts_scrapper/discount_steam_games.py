from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime 

def main():
    current_time = datetime.now().strftime("%Y.%m.%d %Hh%Mm") 
    path = r"PATH\chromedriver.exe"
    driver = webdriver.Chrome(path)


    driver.get("https://gg.deals/deals/steam-deals/?page=1")
    max_page = int(driver.find_element(By.CSS_SELECTOR, "[aria-label='Last page']").text[-1]) + 1


    list_of_titles = []
    list_of_dates = []
    list_of_new_prices = []
    list_of_discounts = []
    list_of_old_prices = []

    for i in range(1, max_page):
        try:
            driver.get("https://gg.deals/deals/steam-deals/?page=" + str(i))
            
            
            titles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "game-info-title-wrapper"))
            )
            list_of_titles += [title.text for title in titles]
            
            
            dates = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//time[@data-original-title]"))
            )
            list_of_dates += [date.get_attribute("data-original-title") for date in dates]
            
            
            new_prices = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "price-inner.game-price-new"))
            )
            list_of_new_prices += [new_price.text for new_price in new_prices]
            
            
            discounts = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "discount.label"))
            )
            list_of_discounts += [discount.text for discount in discounts]
            
            
            old_prices = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "price-label.price-old"))
            )
            list_of_old_prices += [old_price.text for old_price in old_prices]
        
            
        except:
            print("TERMINATED")
            driver.quit()


    for ls in [list_of_titles, list_of_dates, list_of_new_prices, list_of_discounts, list_of_old_prices]:
        ls = list(filter(None, ls))

    
    result = pd.DataFrame(zip(list_of_titles, list_of_new_prices, list_of_discounts, list_of_old_prices, list_of_dates)) 
    result.columns = ["Title","NewPrice", "Discount", "OldPrice", "CreationDate"]
    result.to_csv(f"discounts/{str(current_time)} discounts.csv", index=False)


if __name__ == "__main__":
    main()
