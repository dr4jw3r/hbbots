import logging
import os.path
#
from datetime import datetime
from core.GUI import GUI
from core.hotkeyhandler import HotkeyHandler
#

def setup():
    logs_path = os.path.abspath('./logs')
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    logger = logging.getLogger('hbbot')
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(
        logs_path, datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".log")

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(filename)s]\t%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

if __name__ == "__main__":
    logger = setup()
    try:
        HotkeyHandler().registerhotkeys()
        exit(GUI().buildui())
    except Exception as e:
        logger.error(e)
