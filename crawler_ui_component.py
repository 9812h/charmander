from tkinter import *
from tkinter import font
import threading
from datetime import datetime
import utils
from session_worker import *

class CrawlerUiComponent(Frame):
    def __init__(self, root, crawler, headers=[]):
        super().__init__(root)
        self.root = root
        self.crawler = crawler
        self.headers = headers
        self.strvars_to_update = []
        self.status_strvar = StringVar()
        self.config(
            padx=10,
            pady=10,
            borderwidth=1,
            relief=RIDGE
        )
        self.build_ui()

    def pack(self):
        super().pack(side=TOP, fill=X)
        thread = threading.Thread(target=self.crawler.start, args=())
        thread.start()
        self.update_values()
        self.update_status()

    def build_ui(self):
        header_container = Frame(self)
        header_container.config(pady=5)
        header_container.pack(side=TOP, fill=X)
        title = Label(header_container, anchor=W, text=self.crawler.name)
        title.config(
            font=font.Font(size=12, weight="bold")
        )
        title.pack(side=LEFT)
        export_button = Button(header_container, text="Export", command=self.export_button_callback)
        export_button.config(
            padx=10,
            relief=GROOVE
        )
        export_button.pack(side=RIGHT)

        self.status = Label(self, anchor=W)
        self.status.config(
            textvariable=self.status_strvar,
            font=font.Font(size=10, slant="italic")
        )
        self.status.pack(side=TOP, fill=X)

        for header in self.headers:
            container = Frame(self)
            container.pack(side=TOP, fill=X)
            header_label = Label(container, anchor=W, text=header)
            header_label.pack(side=LEFT, fill=X)
            value_strvar = StringVar()
            self.strvars_to_update.append(value_strvar)
            value_label = Label(container, anchor=E, textvariable=value_strvar)
            value_label.pack(side=RIGHT, fill=X)
            value_strvar.set("N/A")

    def export_button_callback(self):
        self.crawler.export_now()

    def update_status(self):
        try:
            state = self.crawler.get_session_worker_state()
            if state == SessionWorker.FIRST_HALF_STATE or state == SessionWorker.SECOND_HALF_STATE:
                self.status.config(fg="green")
            else:
                self.status.config(fg="red")
            self.status_strvar.set(str(self.crawler.get_session_worker_state()))
        except Exception as e:
            utils.log(e)
        self.root.after(1000, self.update_status)

    def update_values(self):
        lastest_data = (self.crawler.get_lastest_data()).copy()
        if len(lastest_data) > 0:
            lastest_data[0] = datetime.fromtimestamp(float(lastest_data[0])).strftime("%d/%m/%Y %H:%M:%S")
            for i in range(0, len(lastest_data)):
                self.strvars_to_update[i].set(lastest_data[i])
        self.root.after(1000, self.update_values)

