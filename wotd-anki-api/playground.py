import threading
from time import sleep

from src.logic.TimeoutLock import time_limit, TimeoutException

lock = threading.Lock()

def test():
    try:
        with time_limit(3):
            with lock:
                print('before sleep')
                sleep(5)
                print('after sleep')
    except TimeoutException as e:
        print('timed out')


print('before exec')
test()
print('after exec')
