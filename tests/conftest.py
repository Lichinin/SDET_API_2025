import datetime
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest
from faker import Faker

fake = Faker()

from api_client.api_client import ApiClient


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


@pytest.fixture
def entity_data():
    return {
        "addition": {
            "additional_info": fake.sentence(),
            "additional_number": fake.random_int(min=1, max=99)
        },
        "important_numbers": [
            fake.random_int(min=1, max=99),
            fake.random_int(min=1, max=99),
            fake.random_int(min=1, max=99)
        ],
        "title": fake.text(max_nb_chars=15),
        "verified": fake.boolean()
    }

@pytest.fixture
def created_entity_id(entity_data, logger):
    api_client = ApiClient('http://localhost:8080', logger=logger)
    api_client.create_entity(entity_data)
    return api_client.data

