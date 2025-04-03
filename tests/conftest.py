import datetime
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from config import Pathes
import pytest
from faker import Faker

from api_client.api_client import ApiClient
from helpers.data_helpers import DataHelper

fake = Faker()


def pytest_addoption(parser):
    parser.addoption('--log_level', action='store', default="INFO")


@pytest.fixture(scope='function')
def logger(request):
    log_dir = Pathes.LOG_DIR
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
def created_entity_id(logger):
    api_client = ApiClient(logger=logger)
    api_client.create_entity(DataHelper.entity_setup_data())
    return api_client.response_data


@pytest.fixture
def teardown_entity(logger):
    entity_holders = []

    yield entity_holders

    if entity_holders:
        api_client = ApiClient(logger=logger)
        api_client.delete_entity(entity_holders[0])


@pytest.fixture
def new_entity(logger, request):
    api_client = ApiClient(logger=logger)
    entities_id = []
    num_entities = request.param if hasattr(request, "param") else 1
    for _ in range(num_entities):
        api_client.create_entity(DataHelper.entity_setup_data())
        entities_id.append(api_client.response_data)

    yield entities_id[0] if num_entities == 1 else entities_id

    for entity_id in entities_id:
        api_client.delete_entity(entity_id)
