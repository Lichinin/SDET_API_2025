import allure

from api_client.api_client import ApiClient
from helpers.api_helpers import ValidationHelper
from schemas.schemas import EntityModel, EntityListModel, EntityCreateModel


@allure.epic('SimbirSoft SDET practicum')
@allure.suite('API tests')
class TestApi:

    def test_get_entity(self, logger):
        api_client = ApiClient(logger=logger)
        api_client.get_entity_by_id('1')
        ValidationHelper.validate_response_schema(
            EntityModel,
            api_client.response_data,
            api_client.logger
        )

    def test_get_entity_list(self, logger):
        api_client = ApiClient(logger=logger)
        api_client.get_entity_list()
        ValidationHelper.validate_response_schema(
            EntityListModel,
            api_client.response_data,
            api_client.logger
        )

    def test_create_entity(self, entity_data, logger):
        api_client = ApiClient(logger=logger)
        api_client.create_entity(entity_data)
        ValidationHelper.assert_create_entity_response(
            EntityCreateModel,
            api_client.response_data,
            api_client.logger
        )

    def test_edit_entity(self, entity_data, created_entity_id, logger):
        api_client = ApiClient(logger=logger)
        api_client.patch_entity(entity_data, created_entity_id)
        api_client.assert_patch_entity_title(created_entity_id)

    def test_delete_entity(self, created_entity_id, logger):
        api_client = ApiClient(logger=logger)
        api_client.delete_entity(created_entity_id)
        api_client.assert_delete_entity(created_entity_id)
