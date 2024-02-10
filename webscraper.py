from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def getFightersFromPage(ufc_page_source):
    total_links = []
    soup = BeautifulSoup(ufc_page_source, 'html.parser')
    raw_links = soup.find_all('a', class_='b-link b-link_style_black')

    for potential_link in raw_links:
        link = potential_link.get('href')
        total_links.append(link)
    return total_links


def main()
    base_url = 'http://www.ufcstats.com/statistics/fighters?char='
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    driver = webdriver.Firefox()

    for char in letters:
        url = base_url + char + '&page=all'
        driver.get(url)
    
        try:
    
            ufc_page_source = driver.page_source
            print(char, getFightersFromPage(ufc_page_source))
    
       
        except Exception as e:
            print(f"Failed to retrieve data for {char}: {e}")
            exit(1)

    driver.quit()
if __name__ == "__main__":
    main()
