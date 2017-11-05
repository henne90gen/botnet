import logging
import socket
import sys
import time
from contextlib import closing
from threading import Thread
import schedule


def find_free_port():
    if True:
        return 8080
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def setup_logger(app, name):
    app.logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    date_format = '%d/%m/%Y %H:%M:%S'
    message_format = '(%(asctime)s) %(name)s [%(levelname)s]: %(message)s'
    handler.setFormatter(logging.Formatter(message_format, date_format))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return logging.getLogger(name)


def start_scheduler():
    def scheduler():
        while 1:
            schedule.run_pending()
            time.sleep(1)

    Thread(target=scheduler, daemon=True).start()
