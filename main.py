from crawler import *
import utils
import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def random_behavior():
    number = random.randint(1, 5)
    time.sleep(number)
    return number

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
    crawlerConfig = CrawlerConfig(crawling_callback=quantity_crawl)
    quantity_crawler = Crawler(name="quantity", config=crawlerConfig)
    quantity_thread = threading.Thread(target=quantity_crawler.start, args=())
    quantity_thread.start()
    quantity_thread.join()
