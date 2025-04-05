import logging

import allure

from api_client.api_client import ApiClient


class ValidationHelper:

    @staticmethod
    @allure.step('Проверить схему JSON-ответа')
    def validate_via_pydantic(model, response_data):
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
    def check_delited_entity(entity_id, entities_list):
        assert entity_id not in entities_list, \
            f'Deleted entity(ID={entity_id} in entities list)'

    @staticmethod
    @allure.step('Проверить изменение title сущности')
    def check_patched_entity_title(entity_id, original_title):
        api_client = ApiClient()
        response = api_client.get_entity_by_id(entity_id)
        assert response.json()['title'] == f'EDITED_{original_title}', \
            f'Edited title must be "EDITED_{original_title}"'
