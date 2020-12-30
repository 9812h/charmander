from crawler import *
from main_window import *
from crawler_ui_component import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from msedge.selenium_tools.options import Options as EdgeOptions
from msedge.selenium_tools.webdriver import WebDriver as Edge

def stockprice_crawl(state):
    output = []

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
            data.append(col.text.replace(".","").replace(",", "."))

        curr_row_number = float(data[0])
        curr_price = float(data[2])
        curr_diff = float(data[3])
        curr_quantity = float(data[4])
        curr_type = data[5]

        if curr_row_number < 3:
            pass
        else:
            if state["Largest qtty"] < curr_quantity: # =< ?
                state["Largest qtty"] = curr_quantity
                state["Price of largest qtty"] = curr_price
                state["B/S (largest qtty)"] = curr_type

        output = [curr_price, curr_diff, state["Largest qtty"], state["Price of largest qtty"], state["B/S (largest qtty)"]]
    except Exception as e:
        print(e)
    browser.quit()
    return output

if __name__ == '__main__':
    main_window = MainWindow()
    
    stockprice_crawler_config = CrawlerConfig(
        crawling_callback=stockprice_crawl,
        crawling_state={
            "Largest qtty": -1,
            "Price of largest qtty":"N/A",
            "B/S (largest qtty)": "N/A"
        }
    )
    stockprice_crawler = Crawler(config=stockprice_crawler_config, name="stockprice")
    stockprice_ui_component = CrawlerUiComponent(
        main_window,
        stockprice_crawler,
        headers=["Time", "Price", "Current +/-", "Largest qtty", "Price of largest qtty", "B/S (largest qtty)"]
    )
    stockprice_ui_component.pack()
    main_window.mainloop()
