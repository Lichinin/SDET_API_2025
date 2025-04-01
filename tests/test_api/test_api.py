import allure

from api_client.api_client import ApiClient


@allure.epic('SimbirSoft SDET practicum')
@allure.suite('API tests')
class TestApi:

    def test_get_entity(self, logger):
        api_client = ApiClient('http://localhost:8080', logger=logger)
        api_client.get_entity_by_id('1')
        api_client.assert_get_entity_response()

    def test_get_entity_list(self, logger):
        api_client = ApiClient('http://localhost:8080', logger=logger)
        api_client.get_entity_list()
        api_client.assert_get_entity_list_response()

    def test_create_entity(self, entity_data, logger):
        api_client = ApiClient('http://localhost:8080', logger=logger)
        api_client.create_entity(entity_data)
        api_client.assert_create_entity_response()

    def test_edit_entity(self, entity_data, created_entity_id, logger):
        api_client = ApiClient('http://localhost:8080', logger=logger)
        api_client.patch_entity(entity_data, created_entity_id)
        api_client.assert_patch_entity_title(created_entity_id)

    def test_delete_entity(self, created_entity_id, logger):
        api_client = ApiClient('http://localhost:8080', logger=logger)
        api_client.delete_entity(created_entity_id)
        api_client.assert_delete_entity(created_entity_id)