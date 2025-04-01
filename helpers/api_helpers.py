import allure


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
