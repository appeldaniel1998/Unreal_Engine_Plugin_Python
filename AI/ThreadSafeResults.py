import threading
from typing import List


class ThreadSafeResults:
    def __init__(self):
        self.lock = threading.Lock()
        self.results = []

    def update_results(self, new_results):  # for yolo this is a list of YoloDetectionObject
        with self.lock:
            self.results = new_results

    def get_latest_results(self) -> List:
        with self.lock:
            current_results = self.results.copy()  # Make a copy of the current results
            self.results.clear()  # Optionally clear results after fetching to avoid re-processing
            return current_results

    def clear_results(self):
        with self.lock:
            self.results.clear()  # Explicitly clear results when needed

    def append_results(self, new_results):
        with self.lock:
            self.results.append(new_results)  # Append new results to existing list
