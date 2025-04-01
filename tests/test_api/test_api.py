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

    def test_create_entity(self):
        pass

    def test_edit_entity(self):
        pass

    def test_delete_entity(self):
        pass
