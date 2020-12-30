from session_worker import SessionWorker
from session_worker import SessionWorkerConfig
import threading
import utils
import os
from datetime import datetime
import uuid
import csv

class Crawler():
    def __init__(self, config, name=str(uuid.uuid4().hex)):
        self.lastest_timestamp = 0.0
        self.lastest_data = []
        self.name = name
        self.threads = []
        self.config = config
        self.tmp_file = None
        worker_config = SessionWorkerConfig(
            running_delay=5,
            first_half_start_callback=self.start_crawling,
            first_half_running_callback=self.crawl,
            first_half_end_callback=self.finish_crawling,
            second_half_start_callback=self.start_crawling,
            second_half_running_callback=self.crawl,
            second_half_end_callback=self.finish_crawling
        )
        self.session_worker = SessionWorker(worker_config)

    def start(self):
        utils.log("Crawler", "`", self.name, "`", "started")
        self.session_worker.start()

    def start_crawling(self):
        utils.log("Start crawling...")
        self.threads = []
        try:
            os.mkdir("tmp")
        except Exception as e:
            pass
        try:
            os.mkdir("output")
        except Exception as e:
            pass
        self.tmp_filepath = "./tmp/" + datetime.now().strftime("%Y%m%d") + "_" + str(self.session_worker.get_state()) + "_" + self.name + ".tmp"
        self.output_filepath = "./output/" + self.name + "_" + datetime.now().strftime("%Y%m%d") + "_" + str(self.session_worker.get_state()) + ".csv"
        self.tmp_file = open(self.tmp_filepath, "a+", buffering=1)
        self.crawl_cb_state = (self.config.crawling_state).copy()


    def crawl_cb_wrapper(self):
        current_timestamp = datetime.now().timestamp()
        output = utils.execute_callback(self.config.crawling_callback, (self.crawl_cb_state, ))
        utils.log(current_timestamp, output)
        if self.lastest_timestamp < current_timestamp:
            self.lastest_timestamp = current_timestamp
            self.lastest_data = [current_timestamp] + output
        try:
            row = str(current_timestamp)
            for item in output:
                row = row + ";" + str(item)
            self.tmp_file.write(row+"\n")
        except Exception as e:
            utils.log(e)

    def crawl(self):
        thread = threading.Thread(
            target=self.crawl_cb_wrapper,
            args=(),
            name=self.name+"@"+datetime.now().strftime("%Y%m%d")+"_"+str(self.session_worker.get_state())+"#"+str(len(self.threads))
        )
        thread.start()
        self.threads.append(thread)

    def finish_crawling(self):
        for thread in self.threads:
            thread.join()
        try:
            self.tmp_file.close()
        except Exception as e:
            utils.log(e)
        self.export_tmp(self.output_filepath)
        utils.log("Crawling finished.")

    def export_tmp(self, filepath):
        tmp_file = open(self.tmp_filepath, "r")
        data = list(csv.reader(tmp_file, delimiter=";"))
        data.sort(key=lambda x: float(x[0]))
        for x in data:
            x[0] = datetime.fromtimestamp(float(x[0])).strftime("%m/%d/%Y %H:%M:%S")
        output_file = open(filepath, "a+", newline="")
        csv.writer(output_file, delimiter=";").writerows(data)
        try:
            tmp_file.close()
        except Exception as e:
            utils.log(e)
        try:
            output_file.close()
        except Exception as e:
            utils.log(e)

    def get_lastest_data(self):
        return self.lastest_data

    def get_session_worker_state(self):
        return self.session_worker.get_state()

    def export_now(self):
        if not (self.session_worker.get_state() == SessionWorker.WAITING_STATE):
            export_filepath = "./output/"\
                              + "exported_" + datetime.now().strftime("%H%M%S_") \
                              + self.name + "_" + datetime.now().strftime("%Y%m%d") + "_" + str(self.session_worker.get_state()) + ".csv"
            self.export_tmp(export_filepath)
            return export_filepath
        return None

class CrawlerConfig:
    def __init__(self, crawling_callback=None, crawling_state={}):
        self.crawling_callback = crawling_callback
        self.crawling_state = crawling_state

