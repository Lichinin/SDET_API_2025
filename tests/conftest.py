import logging
from logging.handlers import RotatingFileHandler

import pytest

from api_client.api_client import ApiClient
from config import Paths
from helpers.data_helpers import DataHelper


@pytest.fixture(autouse=True)
def configure_logging(request):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    log_dir = Paths.LOG_DIR
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        str(log_dir / f'{request.node.name}.log'),
        maxBytes=30000000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    test_logger = logging.getLogger(request.node.name)
    test_logger.info(f'Test started: {request.node.name}')

    yield

    test_logger.info(f'Test finished: {request.node.name}\n')


@pytest.fixture
def created_entity_id(request, api_client):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup started')
    logger.info('====> Fixture: Try create entity for test')
    response = api_client.create_entity(DataHelper.entity_setup_data())
    logger.info(f'====> Fixture: Successful create entity (id={response.json()}) for test.')
    return response.json()


@pytest.fixture
def teardown_entity(request, api_client):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    entity_holders = []

    yield entity_holders

    if entity_holders:
        for entity in entity_holders:
            logger.info('====> Fixture: Delete entity for test')
            api_client.delete_entity(entity)


@pytest.fixture
def new_entity(request, api_client):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup started')
    entities_list = []
    num_entities = request.param if hasattr(request, 'param') else 1
    for _ in range(num_entities):
        logger.info('====> Fixture: Try create entity for test')
        response = api_client.create_entity(DataHelper.entity_setup_data())
        created_entity_id = response.json()
        logger.info(f'====> Fixture: Successful create entity (id={created_entity_id}) for test.')
        entities_list.append(api_client.get_entity_by_id(created_entity_id).json())

    yield entities_list[0] if num_entities == 1 else entities_list

    for entity in entities_list:
        logger.info(f'====> Fixture: Delete entity (id={entity["id"]}) for test')
        api_client.delete_entity(entity['id'])
    logger.info('====> Fixture setup exit')


@pytest.fixture(scope='function')
def api_client(request):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture ApiClient started')
    client = ApiClient()

    yield client

    logger.info('====> Fixture ApiClient teardown')
