import allure
import requests
from schemas.schemas import EntityModel, EntityListModel


class ApiClient:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    @allure.step('Получение сущности по id')
    def get_entity_by_id(self, id):
        url = self.base_url + f'/api/get/{id}'
        try:
            self.logger.info('* Try to get element by id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Получение сущности по id')
    def get_entity_list(self):
        url = self.base_url + '/api/getAll'
        try:
            self.logger.info('* Try to get element by id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка ответа get-запроса сущности')
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

    @allure.step('Проверка ответа get-запроса получения всех сущностей')
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
