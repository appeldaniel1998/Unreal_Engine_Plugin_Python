import threading


class ThreadSafeResults:
    def __init__(self):
        self.lock = threading.Lock()
        self.results = []

    def update_results(self, new_results):
        with self.lock:
            self.results = new_results

    def get_latest_results(self):
        with self.lock:
            return self.results.copy()  # Return a copy to prevent accidental modifications
