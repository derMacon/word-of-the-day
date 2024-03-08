import logging
import os

LOG_FILENAME = "./logs/output.log"
LOG_LEVEL = logging.DEBUG

os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
logging_format = '%(asctime)s - %(levelname)-6s: %(filename)s %(funcName)s - %(message)s'
file_handler = logging.FileHandler(LOG_FILENAME, mode="a", encoding=None, delay=False)
file_handler.setFormatter(logging.Formatter(logging_format))

logging.basicConfig(
    format=logging_format,
)

log = logging.getLogger('custom_logger')
log.addHandler(file_handler)
log.setLevel(LOG_LEVEL)
