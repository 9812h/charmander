from datetime import datetime
import time
import utils

class SessionWorker:
    WAITING_STATE = "waiting"
    FIRST_HALF_STATE = "first_half"
    SECOND_HALF_STATE = "second_half"

    def __init__(self, config):
        self.config = config
        self.state = None

    def start(self):
        self.idle()

    def idle(self):
        while True:
            if 0 <= datetime.now().isoweekday() <= 5:

                if SessionWorker.is_first_half():
                    utils.execute_callback(self.config.session_start_callback, self.config.session_start_callback)
                    self.state = SessionWorker.FIRST_HALF_STATE
                    utils.execute_callback(self.config.first_half_start_callback, self.config.first_half_start_args)
                    self.work(SessionWorker.is_first_half,
                                       self.config.running_delay,
                                       self.config.half_running_callback,
                                       self.config.half_running_args,
                                       self.config.first_half_running_callback,
                                       self.config.first_half_running_args)
                    utils.execute_callback(self.config.first_half_end_callback, self.config.first_half_end_args)

                else:
                    if SessionWorker.is_second_half():
                        self.state = SessionWorker.SECOND_HALF_STATE
                        utils.execute_callback(self.config.second_half_start_callback, self.config.second_half_start_args)
                        self.work(SessionWorker.is_second_half,
                                           self.config.running_delay,
                                           self.config.half_running_callback,
                                           self.config.half_running_args,
                                           self.config.second_half_running_callback,
                                           self.config.second_half_running_args)
                        utils.execute_callback(self.config.second_half_end_callback, self.config.second_half_end_args)
                        utils.execute_callback(self.config.session_end_callback, self.config.session_end_args)
                    else:
                        self.state = SessionWorker.WAITING_STATE
            else:
                self.wait()

    def work(self, half_running_condition, running_delay, all_half_callback, all_half_args, callback, args):
        while True:
            if not half_running_condition():
                break
            utils.execute_callback(all_half_callback, all_half_args)
            utils.execute_callback(callback, args)
            time.sleep(running_delay)

    def wait(self):
        while True:
            if (SessionWorker.is_first_half()) or (SessionWorker.is_second_half()):
                break
            time.sleep(self.config.running_delay)


    def get_state(self):
        return self.state


    @staticmethod
    def is_first_half():
        curr_hour = datetime.now().hour
        curr_minute = datetime.now().minute
        if (9 <= curr_hour < 11) or (11 == curr_hour and 30 >= curr_minute):
            return True
        return False

    @staticmethod
    def is_second_half():
        curr_hour = datetime.now().hour
        curr_minute = datetime.now().minute
        if (13 <= curr_hour < 14) or (14 == curr_hour and 45 >= curr_minute):
            return True
        return False

    @staticmethod
    def is_halftime():
        curr_hour = datetime.now().hour
        curr_minute = datetime.now().minute
        if (11 == curr_hour and 30 < curr_minute) or (12 == curr_hour):
            return True
        return False


class SessionWorkerConfig:
    def __init__(self,
                 running_delay=5,
                 half_running_callback=None, half_running_args=(),
                 session_start_callback=None, session_start_args=(),
                 first_half_start_callback=None, first_half_start_args=(),
                 first_half_running_callback=None, first_half_running_args=(),
                 first_half_end_callback=None, first_half_end_args=(),
                 second_half_start_callback=None, second_half_start_args=(),
                 second_half_running_callback=None, second_half_running_args=(),
                 second_half_end_callback=None, second_half_end_args=(),
                 session_end_callback=None, session_end_args=()):

        self.running_delay = running_delay

        self.half_running_callback = half_running_callback
        self.half_running_args = half_running_args

        self.session_start_callback = session_start_callback
        self.session_start_args = session_start_args

        self.first_half_start_callback = first_half_start_callback
        self.first_half_start_args = first_half_start_args
        self.first_half_running_callback = first_half_running_callback
        self.first_half_running_args = first_half_running_args
        self.first_half_end_callback = first_half_end_callback
        self.first_half_end_args = first_half_end_args

        self.second_half_start_callback = second_half_start_callback
        self.second_half_start_args = second_half_start_args
        self.second_half_running_callback = second_half_running_callback
        self.second_half_running_args = second_half_running_args
        self.second_half_end_callback = second_half_end_callback
        self.second_half_end_args = second_half_end_args

        self.session_end_callback = session_end_callback
        self.session_end_args = session_end_args

