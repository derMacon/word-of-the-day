from threading import Thread
from threading import Lock


# thread safe counter class
class ThreadSafeCounter:
    """
    src: https://superfastpython.com/thread-safe-counter-in-python/
    """

    # constructor
    def __init__(self):
        # initialize counter
        self._counter = 0
        # initialize lock
        self._lock = Lock()

    # increment the counter
    def increment(self):
        with self._lock:
            self._counter += 1
            return self._counter

    # get the counter value
    def value(self):
        with self._lock:
            return self._counter
