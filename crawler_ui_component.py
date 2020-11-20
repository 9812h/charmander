from tkinter import *
import threading
import utils
import random
import time
from datetime import datetime

class CrawlerUiComponent(Frame):
    def __init__(self, root, crawler, headers = []):
        super().__init__(root)
        self.root = root
        self.crawler = crawler
        self.headers = headers
        self.build_ui()

    def update_values(self):
        lastest_data = self.crawler.get_lastest_data()
        if len(lastest_data) > 0:
            lastest_data[0] = datetime.fromtimestamp(float(lastest_data[0])).strftime("%d/%m/%Y %H:%M:%S")
            for i in range(0, len(lastest_data)):
                self.strvars_to_update[i].set(lastest_data[i])
        self.root.after(1000, self.update_values)


    def build_ui(self):
        title = Label(self, text=self.crawler.name)
        title.pack(side=TOP)
        self.strvars_to_update = []
        for header in self.headers:
            container = Frame(self)
            container.pack(side=TOP)
            header_label = Label(container, text=header)
            header_label.pack(side=LEFT)
            value_strvar = StringVar()
            self.strvars_to_update.append(value_strvar)
            value_label = Label(container, textvariable=value_strvar)
            value_label.pack(side=RIGHT)

        export_button = Button(self, text="Export")
        export_button.pack(side=RIGHT)


    def pack(self):
        super().pack(side=TOP)
        thread = threading.Thread(target=self.crawler.start, args=())
        thread.start()
        self.update_values()

