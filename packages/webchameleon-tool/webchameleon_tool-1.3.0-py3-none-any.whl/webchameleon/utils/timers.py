import time
import random


class AdaptiveTimer:
    def __init__(self):
        self.start_time = None
        self.block_history = []

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.start_time = None

    def elapsed(self) -> float:
        return time.time() - self.start_time if self.start_time else 0.0

    def adaptive_delay(self, status_code: int) -> float:
        self.block_history.append(status_code)
        if len(self.block_history) > 5:
            self.block_history.pop(0)
        block_freq = (
            sum(1 for code in self.block_history if code >= 400)
            / len(self.block_history)
            if self.block_history
            else 0
        )
        base_delay = random.uniform(5, 15)
        return base_delay * (1 + block_freq * 2)
