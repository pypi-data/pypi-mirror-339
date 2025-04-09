import concurrent.futures
import time


class JobInfo:
    def __init__(self, job_id: str, future: concurrent.futures.Future):
        self.future: concurrent.futures = future
        self.job_id: str = job_id
        self.polled_after_done: bool = False
        self.intermediate_events: list = []
        self.timestamp_seconds: time = time.time()

    def is_older(self, delay_seconds: int):
        return time.time() - self.timestamp_seconds > delay_seconds
