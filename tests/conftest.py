import datetime
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--url', action='store', default='http://tech-avito-intern.jumpingcrab.com')
    parser.addoption('--log_level', action='store', default="INFO")
    parser.addoption('--executor', action='store')
    parser.addoption('--browser_version', action='store')


@pytest.fixture(scope='function')
def logger(request):
    log_dir = Path(__file__).parent / 'log'
    log_dir.mkdir(exist_ok=True)
    log_level = request.config.getoption('--log_level')
    browser_name = request.config.getoption('--browser')
    logger = logging.getLogger(request.node.name)
    file_handler = RotatingFileHandler(
        str(log_dir / f'{request.node.name}({browser_name}).log'),
        maxBytes=30000000,
        backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info('===> Test %s started at %s' % (request.node.name, datetime.datetime.now()))

    yield logger

    logger.info('===> Test %s finished at %s' % (request.node.name, datetime.datetime.now()))

    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()
