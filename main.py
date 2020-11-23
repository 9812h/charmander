import utils
import random
import time
from crawler import *
from main_window import *
from crawler_ui_component import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def random_behavior(state):
    number = random.randint(1, 100)
    time.sleep(random.randint(1, 5))
    if state["biggest"] <= number:
        state["biggest"] = number
    return [number, state["biggest"]]

def random_behavior2(state):
    number1 = random.randint(1, 100)
    number2 = random.randint(1, 100)
    time.sleep(random.randint(1, 5))
    return [number1, number2]
def quantity_crawl():
    output = [],
    prefix = "VN30F" + datetime.now().strftime("%y") + str(int(datetime.now().strftime("%m")) + 1)
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.add_argument("--no-sandbox")
    chrome = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)
    chrome.get("https://banggia.hnx.vn/")
    try:
        WebDriverWait(chrome, 200).until(expected_conditions.element_to_be_clickable((By.ID, "PS")))
        chrome.find_element_by_id("PS").click()
        WebDriverWait(chrome, 200).until(expected_conditions.element_to_be_clickable((By.ID, "derivative_details")))
        chrome.find_element_by_id("derivative_details").click()
        WebDriverWait(chrome, 200).until(expected_conditions.element_to_be_clickable((By.ID, prefix + "_last_price")))
        last_price_data = chrome.find_element_by_id(prefix + "_last_price").text
        WebDriverWait(chrome, 200).until(expected_conditions.element_to_be_clickable((By.ID, prefix + "_total_qtty_traded")))
        total_qtty_traded_data = chrome.find_element_by_id(prefix + "_total_qtty_traded").text
        output = [last_price_data, total_qtty_traded_data]
    except TimeoutException:
        utils.log("Timeout!")
    except Exception as e:
        utils.log("Unexpected Exception.")
        utils.log(e)
    chrome.quit()
    return output

if __name__ == '__main__':
    crawlerConfig = CrawlerConfig(crawling_callback=random_behavior, crawling_state={"biggest": -1})
    random_crawler = Crawler(config=crawlerConfig, name="one")

    crawlerConfig = CrawlerConfig(crawling_callback=random_behavior2)
    random_crawler2 = Crawler(config=crawlerConfig, name="two")

    main_window = MainWindow()
    c = CrawlerUiComponent(main_window, random_crawler, headers=["update_time", "this_number", "biggest_number"])
    c.pack()
    c2 = CrawlerUiComponent(main_window, random_crawler2, headers=["update_time", "last_price", "total_qtty_traded"])
    c2.pack()
    main_window.mainloop()