from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

import time

BASS_URL = "https://www.vivino.com"

RED_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1NFDLTaywNTFQS660DQ1WSwYSLmoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWKBksa2zIwDZzhVu"
WINE_URL = "https://www.vivino.com/quinta-do-crasto-vinha-maria-teresa/w/1293594?year=2017&price_id=23982317"
ROSE_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1NlXLTaywNTQxUEuutPX0UUsGEsFqBUDp9DTbssSizNSSxBy1_KIUW7X8pEpbtfKS6FhbEwB9ZRQ4"
DESSERT_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1NlXLTaywNTQxUEuutPX0UUsGEsFqBUDp9DTbssSizNSSxBy1_KIUW7X8pEpbtfKS6FhbcwB9aBQ7"
FORTIFIED_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1MjZQS6609fRRSwYSwWoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWFsjEwCCnhQy"
SPARKLING_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1MjZQS6609fRRSwYSwWoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWFtjAG5tE_8%3D"
WHITE_URL = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1MjZQS6609fRRSwYSwWoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWFsjAG5sE_4%3D"

def scroll_down(body, rols):
    for _ in range(rols):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)


def start():
    ser = Service("./chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('lang=en_US.utf8')
    driver = webdriver.Chrome(service=ser, options=options)
    df = pd.DataFrame()
    for link in get_wine_links(driver, WHITE_URL):
        try:
            df = df.append(get_wine_info(driver, link))
        except:
            print("link failed")
    print(df)
    df.to_csv("./white.csv")


def get_wine_links(driver, url):
    driver.get(url)
    simpleLabel = driver.find_element(By.CLASS_NAME, "simpleLabel__label--4j3ek")
    simpleLabel.click()
    shipToDropdown = driver.find_elements(By.CLASS_NAME, "shipToDropdown__item--AWsOZ")[-1]
    shipToDropdown.click()
    time.sleep(2)
    body = driver.find_element(By.TAG_NAME, "body")
    scroll_down(body, 300)
    explorer_page_results = body.find_element(By.CLASS_NAME, "explorerPage__results--3wqLw")
    links_elements = explorer_page_results.find_elements(By.TAG_NAME, r"a")
    links_unfilter = [links_element.get_attribute('href') for links_element in links_elements]
    links = [link for link in links_unfilter if link is not None and '/w/' in link]
    return links


def get_wine_info(driver, url):
    res = dict()
    driver.get(url)
    body = driver.find_element(By.TAG_NAME, "body")
    scroll_down(body, 15)
    ratings = driver.find_element(By.CLASS_NAME, "vivinoRating__averageValue--3Navj")
    res["ratings"] = [ratings.text]
    tbody = driver.find_element(By.TAG_NAME, "tbody")
    # country_name = driver.find_element(By.CLASS_NAME, "wineTasteStyle-desktop__countryName--21k53")
    # res["country_name"] = [country_name.text]
    # wine_name = driver.find_element(By.CLASS_NAME, "wineTasteStyle-desktop__wineName--ML0zS")
    # res["wine_name"] = [wine_name.text]

    rows = tbody.find_elements(By.TAG_NAME, "tr")
    vals = ["Bold", "Tannic", "Sweet", "Acidic"]
    for row, val in zip(rows, vals):
        s = row.find_element(By.CLASS_NAME, "indicatorBar__progress--3aXLX")
        res[val] = [s.get_attribute('style').split(' ')[-1]]

    wineFacts = driver.find_elements(By.CLASS_NAME, "wineFacts__wineFacts--2Ih8B")[-1]
    for wineFact in wineFacts.find_elements(By.TAG_NAME, "tr"):
        name = wineFact.find_element(By.TAG_NAME, "th")
        val = wineFact.find_element(By.TAG_NAME, "td")
        res[name.text] = [val.text]
    return pd.DataFrame(res)


if __name__ == "_main_":
    start()