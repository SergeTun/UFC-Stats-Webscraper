from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

base_url = 'http://www.ufcstats.com/statistics/fighters?char='
letters = 'abcdefghijklmnopqrstuvwxyz'
driver = webdriver.Chrome()

for char in letters:
    url = base_url + char + '&page=all'
    driver.get(url)

    try:

        fighter_links = driver.find_elements(By.CLASS_NAME, 'b-link.b-link_style_black')

        for link in fighter_links:
            fighter_name = link.text
            link.click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.back()
    
    except Exception as e:
        print(f"Failed to retrieve data for {char}: {e}")

driver.quit()
