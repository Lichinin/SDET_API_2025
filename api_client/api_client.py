import allure
import requests

from config import APiRoutes
from schemas.schemas import EntityCreateModel, EntityListModel, EntityModel


class ApiClient:
    def __init__(self, logger):
        self.logger = logger

    @allure.step('Получение сущности по id')
    def get_entity_by_id(self, id):
        url = APiRoutes.entity_by_id_url(id)
        try:
            self.logger.info('* Try to get entity by id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get entity by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get entity by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Получение всех сущностей по id')
    def get_entity_list(self):
        url = APiRoutes.entity_list_url()
        try:
            self.logger.info('* Try to get entities list')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get entities list'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get entities list'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка создания сущности')
    def create_entity(self, entity_data):
        url = APiRoutes.create_entity_url()
        headers = {
            "Content-Type": "application/json"
        }
        try:
            self.logger.info('* Try to create entity')
            response = requests.post(
                url,
                headers=headers,
                json=entity_data
            )
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed create entity'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed create entity'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка редактирования сущности')
    def patch_entity(self, entity_data, entity_id):
        url = APiRoutes.patch_entity_url(entity_id)
        headers = {
            "Content-Type": "application/json"
        }
        entity_data['title'] = f'EDITED_{entity_data["title"]}'
        try:
            self.logger.info('* Try to path entity')
            response = requests.patch(
                url,
                headers=headers,
                json=entity_data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed patch entity'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed patch entity'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка удаления сущности')
    def delete_entity(self, entity_id):
        url = APiRoutes.delete_entity_url(entity_id)
        headers = {
            "Content-Type": "text/plain"
        }
        try:
            self.logger.info('* Try to delete entity by id')
            response = requests.delete(
                url,
                headers=headers
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed delete entity by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed delete entity by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Валидация ответа get-запроса сущности')
    def assert_get_entity_response(self):
        self.logger.info('* Check response scheme')
        try:
            EntityModel(**self.data)
            self.logger.info(self.data)
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        self.logger.info(self.data)

    @allure.step('Валидация ответа get-запроса получения всех сущностей')
    def assert_get_entity_list_response(self):
        self.logger.info('* Check response scheme')
        try:
            EntityListModel(**self.data)
            self.logger.info(self.data)
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        self.logger.info(self.data)

    @allure.step('Валидация ответа post-запроса создания сущности')
    def assert_create_entity_response(self):
        self.logger.info('* Check response scheme')
        try:
            EntityCreateModel(self.data)
            self.logger.info(self.data)
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        self.logger.info(self.data)

    @allure.step('Проверка отсутствия удаленной сущности в БД')
    def assert_delete_entity(self, entity_id):
        self.get_entity_list()
        entities_id = [item["id"] for item in self.data["entity"]]
        assert entity_id not in entities_id

    @allure.step('Проверка изменения title сущности')
    def assert_patch_entity_title(self, entity_id):
        self.get_entity_by_id(entity_id)
        assert self.data['title'].startswith('EDITED_')
