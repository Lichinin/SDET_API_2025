import logging

import allure

from api_client.api_client import ApiClient


class ValidationHelper:

    @staticmethod
    @allure.step('Проверить схему JSON-ответа')
    def validate_via_pydantic(
        model: type,
        response_data: dict | list[dict]
    ) -> None:
        logger = logging.getLogger(f'validation.{model.__name__}')
        logger.info('* Check response scheme')
        try:
            if isinstance(response_data, dict):
                model(**response_data)
            else:
                model(response_data)
            logger.info(f'entity data: {response_data}')
            logger.info('* Scheme is valid.')
        except Exception as e:
            error_msg = f'Validation error: {str(e)}'
            logger.error(error_msg)
            raise AssertionError(error_msg)


class AssertionHelper:

    @staticmethod
    @allure.step('Проверить отсутствие удаленной сущности')
    def check_deleted_entity(
        entity_id: int,
        entities_list: list[int]
    ) -> None:
        assert entity_id not in entities_list, \
            f'Deleted entity(ID={entity_id} in entities list)'

    @staticmethod
    @allure.step('Получить title сущности')
    def get_entity_title(entity_id: int) -> str:
        api_client = ApiClient()
        response = api_client.get_entity_by_id(entity_id)
        return response.json()['title']

    @staticmethod
    @allure.step('Получить title сущности')
    def check_getting_created_entity_data(
        created_entity: dict | list[dict],
        list_of_all_entities: list[dict]
    ) -> None:
        for entity in created_entity:
            assert entity in list_of_all_entities, \
                'Созданная сущность отсутствует в списке всех сущностей'

    @staticmethod
    @allure.step('Проверить статус-код ответа')
    def check_status_code(
        actual_status_code: int,
        expected_status_code: int
    ):
        assert actual_status_code == expected_status_code, \
                f'Excepted status code {expected_status_code}, got {actual_status_code}'
