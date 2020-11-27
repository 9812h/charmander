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

from msedge.selenium_tools.options import Options as EdgeOptions
from msedge.selenium_tools.webdriver import WebDriver as Edge

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

def hnx_crawl(state):
    output = [],
    prefix = "VN30F" + datetime.now().strftime("%y") + str(int(datetime.now().strftime("%m")) + 1)

    ### Chrome
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--no-sandbox")
    # browser = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)

    ### Firefox
    # options = webdriver.FirefoxOptions()
    # options.headless = True
    # browser = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)

    ### MS Edge (Chromium)
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("headless")
    # options.add_argument("disable-gpu")
    browser = Edge(executable_path="./drivers/msedgedriver", options=options)

    browser.get("https://banggia.hnx.vn/")
    try:
        WebDriverWait(browser, 200).until(expected_conditions.element_to_be_clickable((By.ID, "PS")))
        browser.find_element_by_id("PS").click()
        WebDriverWait(browser, 200).until(expected_conditions.element_to_be_clickable((By.ID, "derivative_details")))
        browser.find_element_by_id("derivative_details").click()
        WebDriverWait(browser, 200).until(expected_conditions.element_to_be_clickable((By.ID, prefix + "_last_price")))
        last_price_data = browser.find_element_by_id(prefix + "_last_price").text
        WebDriverWait(browser, 200).until(expected_conditions.element_to_be_clickable((By.ID, prefix + "_total_qtty_traded")))
        total_qtty_traded_data = browser.find_element_by_id(prefix + "_total_qtty_traded").text
        output = [last_price_data, total_qtty_traded_data]
    except Exception as e:
        utils.log(e)
    browser.quit()
    return output

def stockprice_crawl(state):
    output = []

    ### Chrome
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--no-sandbox")
    # browser = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)

    ### Firefox
    # options = webdriver.FirefoxOptions()
    # options.headless = True
    # browser = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)

    ### MS Edge (Chromium)
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    browser = Edge(executable_path="./drivers/msedgedriver", options=options)

    browser.get("http://stockprice.vn/a/mix.html")
    try:
        WebDriverWait(browser, 100).until(expected_conditions.element_to_be_clickable((By.ID, "combobox-1013-inputEl")))
        browser.find_element_by_id("combobox-1013-inputEl").send_keys("VN30F1M")
        # WebDriverWait(browser, 100).until(expected_conditions.e((By.ID, "btnDetail")))
        time.sleep(5)
        browser.find_element_by_id("btnDetail").click()
        WebDriverWait(browser, 100).until(expected_conditions.element_to_be_clickable((By.ID, "tblDealHist0")))
        rows = browser.find_element_by_id("tblDealHist0").find_elements(By.TAG_NAME, "tr")
        cols = rows[0].find_elements(By.TAG_NAME, "td")
        data = []
        for col in cols:
            data.append(col.text.replace(",", "."))

        curr_price = float(data[2])
        curr_diff = float(data[3])
        curr_quantity = float(data[4])
        curr_type = data[5]

        if state["largest_quantity"] < curr_quantity:
            state["largest_quantity"] = curr_quantity
            state["type"] = curr_type
        output = [curr_price, curr_diff, state["largest_quantity"], state["type"]]
    except Exception as e:
        print(e)
    browser.quit()

    return output


if __name__ == '__main__':
    main_window = MainWindow()
    hnx_crawler_config = CrawlerConfig(crawling_callback=hnx_crawl, crawling_state={})
    hnx_crawler = Crawler(config=hnx_crawler_config, name="hnx")
    hnx_ui_component = CrawlerUiComponent(main_window, hnx_crawler, headers=["update_time", "last_price", "total_qtty_traded"])
    # hnx_ui_component.pack()
    
    stockprice_crawler_config = CrawlerConfig(
        crawling_callback=stockprice_crawl,
        crawling_state={
            "largest_quantity": -1,
            "type": "N/A"
        }
    )
    stockprice_crawler = Crawler(config=stockprice_crawler_config, name="stockprice")
    stockprice_ui_component = CrawlerUiComponent(
        main_window,
        stockprice_crawler,
        headers=["update_time", "price", "diff", "largest_qtty", "type"]
    )
    stockprice_ui_component.pack()
    main_window.mainloop()
