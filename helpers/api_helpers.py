import allure

from api_client.api_client import ApiClient


class ValidationHelper:

    @staticmethod
    @allure.step('Валидация схемы json-ответа')
    def validate_response_schema(model, response_data, logger):
        logger.info('* Check response scheme')
        try:
            model(**response_data) if isinstance(response_data, dict) else model(response_data)
            logger.info(response_data)
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info(response_data)


class AssertionHelper:

    @staticmethod
    @allure.step('Проверка отсутствия удаленной сущности в БД')
    def check_delited_entity(entity_id, entities_list):
        assert entity_id not in entities_list

    @staticmethod
    @allure.step('Проверка изменения title сущности')
    def check_patched_entity_title(entity_id, logger):
        api_client = ApiClient(logger=logger)
        api_client.get_entity_by_id(entity_id)
        assert api_client.response_data['title'].startswith('EDITED_')
