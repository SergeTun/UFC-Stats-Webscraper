from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

base_url = 'http://www.ufcstats.com/statistics/fighters?char='
letters = 'abcdefghijklmnopqrstuvwxyz'
path = '/Users/Serge/Downloads/chromedriver-win64/chromedriver.exe'

driver = webdriver.Chrome(path)

for char in letters:
    url = base_url + char + '&page=all'
    driver.get(url)

    try: 
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.b-statistics__table')))

        fighter_links = driver.find_elements_by_css_selector('a.b-link_style_black')

        for link in fighter_links:
            fighter_name = link.text
            link.click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.back()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.b-statistics__table')))
    
    except Exception as e:
        print(f"Failed to retrieve data for {char}: {e}")

driver.quit()
