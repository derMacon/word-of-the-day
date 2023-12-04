import logging
import os

APP_LOG_FILENAME = "./tmp/logs/app.logs"
APP_LOG_LEVEL = logging.DEBUG

SQL_LOG_FILENAME = "./tmp/logs/sql.logs"
SQL_LOG_LEVEL = logging.DEBUG


def configure_logger(logger_name, log_file, log_level):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging_format = '%(asctime)s - %(levelname)-6s: %(filename)s %(funcName)s - %(message)s'
    file_handler = logging.FileHandler(log_file, mode="a", encoding=None, delay=False)
    file_handler.setFormatter(logging.Formatter(logging_format))

    logging.basicConfig(
        format=logging_format,
    )

    log = logging.getLogger(logger_name)
    log.addHandler(file_handler)
    log.setLevel(log_level)
    return log


app_log = configure_logger(logger_name='app_log', log_file=APP_LOG_FILENAME, log_level=APP_LOG_LEVEL)
sql_log = configure_logger(logger_name='sql_log', log_file=SQL_LOG_FILENAME, log_level=SQL_LOG_LEVEL)
