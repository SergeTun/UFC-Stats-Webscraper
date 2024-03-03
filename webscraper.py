from selenium import webdriver
from bs4 import BeautifulSoup
import json


def getFightersFromPage(ufc_page_source):
    total_links = []
    soup = BeautifulSoup(ufc_page_source, 'html.parser')
    raw_links = soup.find_all('a', class_='b-link b-link_style_black')

    for potential_link in raw_links:
        link = potential_link.get('href')
        if link not in total_links:
            total_links.append(link)

    return total_links



def getFighterStatsFromPage(fighter_source):
    fighter_stat = [0, 0]
    soup = BeautifulSoup(fighter_source, 'html.parser')


    player_name = soup.find('span', class_='b-content__title-highlight').text
    player_name = player_name.strip()
 
 
    games_source = soup.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
 
    for element in games_source:
        wl = element.find('i', class_='b-flag__text').text

        if wl.lower().strip() == 'win':
            fighter_stat[0] += 1

        elif wl.lower().strip() == 'loss':
            fighter_stat[1] += 1

    return { player_name : fighter_stat }




def updateFighter(data, fighter_data):
    fighter, new_stats = list(fighter_data.items())[0]

    stats = data[fighter]
    stats[0] += new_stats[0]
    stats[1] += new_stats[1]

def partialSave(data, file):
    with open(file, 'w') as f:
        f.write(json.dumps(data))




def main():
    base_url = 'http://www.ufcstats.com/statistics/fighters?char='
    letters = 'abcdefghijklmnopqrstuvwxyz'

    results = {}

    driver = webdriver.Firefox()

    for char in letters:
        url = base_url + char + '&page=all'
        driver.get(url)
    
        try:
    
            ufc_page_source = driver.page_source
            links = getFightersFromPage(ufc_page_source)

            for link in links:
                driver.get(link)
                fighter_source = driver.page_source

                fighter_stat = getFighterStatsFromPage(fighter_source)

                if list(fighter_stat.keys())[0] in results:
                    updateFighter(results, fighter_stat)

                else:
                    results.update(fighter_stat)

                partialSave(results, 'fighters.json')
                
        except Exception as e:
            print(f"Failed to retrieve data for {char}: {e}")
            exit(1)

    driver.quit()

if __name__ == "__main__":
    main()
