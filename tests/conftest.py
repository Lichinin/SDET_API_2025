import datetime
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest
from faker import Faker

from api_client.api_client import ApiClient

fake = Faker()


def pytest_addoption(parser):
    parser.addoption('--log_level', action='store', default="INFO")


@pytest.fixture(scope='function')
def logger(request):
    log_dir = Path(__file__).parent / 'log'
    log_dir.mkdir(exist_ok=True)
    log_level = request.config.getoption('--log_level')
    logger = logging.getLogger(request.node.name)
    file_handler = RotatingFileHandler(
        str(log_dir / f'{request.node.name}.log'),
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
def entity_setup_data():
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
def created_entity_id(entity_setup_data, logger):
    api_client = ApiClient(logger=logger)
    api_client.create_entity(entity_setup_data)
    return api_client.response_data


@pytest.fixture
def teardown_entity(logger):
    entity_holder = {'id': None}

    yield entity_holder

    if entity_holder['id'] is not None:
        api_client = ApiClient(logger=logger)
        api_client.delete_entity(entity_holder['id'])
