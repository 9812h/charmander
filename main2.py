from crawler import *
import utils
import random
import time
import threading
from main_window import *
from crawler_ui_component import *

def random_behavior():
    number1 = random.randint(1, 100)
    number2 = random.randint(1, 100)
    time.sleep(random.randint(1, 5))
    return [number1, number2]

if __name__ == '__main__':
    crawlerConfig = CrawlerConfig(crawling_callback=random_behavior)
    random_crawler = Crawler(config=crawlerConfig)
    random_crawler2 = Crawler(config=crawlerConfig)

    main_window = MainWindow()

    c = CrawlerUiComponent(main_window, random_crawler, headers=["update_time", "last_price", "total_qtty_traded"])
    c.pack()

    c2 = CrawlerUiComponent(main_window, random_crawler2, headers=["update_time", "last_price", "total_qtty_traded"])
    c2.pack()

    main_window.mainloop()
