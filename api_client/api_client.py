import allure

from config import APiRoutes
from api_client.base_api_client import BaseApiClient


class ApiClient(BaseApiClient):
    def __init__(self, logger):
        self.logger = logger

    @allure.step('Получить сущность по ID')
    def get_entity_by_id(self, id):
        url = APiRoutes.entity_by_id_url(id)
        self._get(url)

    @allure.step('Получить список всех сущностей')
    def get_entity_list(self):
        url = APiRoutes.entity_list_url()
        self._get(url)

    @allure.step('Создать новую сущность')
    def create_entity(self, entity_data):
        url = APiRoutes.create_entity_url()
        self._post(url, json=entity_data)

    @allure.step('Редактировать сущность по ID')
    def patch_entity(self, entity_data, entity_id):
        url = APiRoutes.patch_entity_url(entity_id)
        entity_data['title'] = f'EDITED_{entity_data["title"]}'
        self._patch(url, json=entity_data)

    @allure.step('Удалить сущность по ID')
    def delete_entity(self, entity_id):
        url = APiRoutes.delete_entity_url(entity_id)
        self._delete(url)

    @allure.step('Получить список ID всех сущностей')
    def get_entities_id_list(self):
        self.get_entity_list()
        return [item["id"] for item in self.response_data["entity"]]
