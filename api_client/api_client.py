import allure
import requests

from api_client.base_api_client import BaseApiClient
from config import APiRoutes


class ApiClient(BaseApiClient):

    @allure.step('Получить сущность по ID')
    def get_entity_by_id(self, entity_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/get/{entity_id}'
        return self._get(url)

    @allure.step('Получить список всех сущностей')
    def get_entity_list(self) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/getALL'
        return self._get(url)

    @allure.step('Создать новую сущность')
    def create_entity(self, entity_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/create'
        return self._post(url, json=entity_data)

    @allure.step('Редактировать сущность по ID')
    def patch_entity(self, entity_data: dict, entity_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/patch/{entity_id}'
        return self._patch(url, json=entity_data)

    @allure.step('Удалить сущность по ID')
    def delete_entity(self, entity_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/delete/{entity_id}'
        return self._delete(url)

    @allure.step('Получить список ID всех сущностей')
    def get_entities_id_list(self) -> list[int]:
        response = self.get_entity_list()
        return [item['id'] for item in response.json()['entity']]
