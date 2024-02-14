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


def main():
    base_url = 'http://www.ufcstats.com/statistics/fighters?char='
    letters = 'abcdefghijklmnopqrstuvwxyz'
    results = []
    losses = 0
    wins = 0
    driver = webdriver.Firefox()

    for char in letters:
        url = base_url + char + '&page=all'
        driver.get(url)
    
        try:
    
            ufc_page_source = driver.page_source
            for link in getFightersFromPage(ufc_page_source):
                driver.get(link)
                soup = BeautifulSoup(ufc_page_source, 'html.parser')
                wl_elements = soup.select('td.b-fight-details__table-col')
                for wl_element in wl_elements:
                    flag_text_element = wl_element.select_one('.b-flag__text')
                    if flag_text_element:
                        result = flag_text_element.get_text(strip=True)
                        results.append(result)
                        for result in results:
                            if result == 'loss':
                                losses += 1
                            else:
                                wins += 1
                    else:
                        print("Element not found")

                print(results)


    
       
        except Exception as e:
            print(f"Failed to retrieve data for {char}: {e}")
            exit(1)

    driver.quit()
if __name__ == "__main__":
    main()
