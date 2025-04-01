import allure
import requests

from config import APiRoutes


class ApiClient:
    def __init__(self, logger):
        self.logger = logger

    @allure.step('Получить сущность по ID')
    def get_entity_by_id(self, id):
        url = APiRoutes.entity_by_id_url(id)
        try:
            self.logger.info('* Try to get entity by id')
            response = requests.get(url)
            response.raise_for_status()
            self.response_data = response.json()
        except requests.exceptions.RequestException:
            self.logger.error(
                f'Failed get entity by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get entity by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Получить список всех сущностей')
    def get_entity_list(self):
        url = APiRoutes.entity_list_url()
        try:
            self.logger.info('* Try to get entities list')
            response = requests.get(url)
            response.raise_for_status()
            self.response_data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get entities list'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get entities list'
                f'(status code = {response.status_code})'
            )

    @allure.step('Создать новую сущность')
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
            self.response_data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed create entity'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed create entity'
                f'(status code = {response.status_code})'
            )

    @allure.step('Редактировать сущность по ID')
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

    @allure.step('Удалить сущность по ID')
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

    @allure.step('Получить список ID всех сущностей')
    def get_entities_id_list(self):
        self.get_entity_list()
        return [item["id"] for item in self.response_data["entity"]]
