import allure
import pytest

from api_client.api_client import ApiClient
from helpers.api_helpers import ValidationHelper, AssertionHelper
from helpers.data_helpers import DataHelper
from schemas.schemas import EntityModel, EntityListModel, EntityCreateModel


@allure.epic('SimbirSoft SDET practicum')
@allure.suite('API tests')
class TestApi:

    @allure.story('Получение сущности')
    @allure.title('Проверка получения сущности по ID')
    def test_get_entity(self, setup_and_teardown_entity, logger):
        api_client = ApiClient(logger=logger)
        api_client.get_entity_by_id(setup_and_teardown_entity)
        ValidationHelper.validate_via_pydantic(
            EntityModel,
            api_client.response_data,
            api_client.logger
        )

    @pytest.mark.parametrize("setup_and_teardown_entity", [3], indirect=True)
    @allure.story('Получение списка сущностей')
    @allure.title('Проверка получения списка сущностей')
    def test_get_entity_list(self, setup_and_teardown_entity, logger):
        api_client = ApiClient(logger=logger)
        api_client.get_entity_list()
        ValidationHelper.validate_via_pydantic(
            EntityListModel,
            api_client.response_data,
            api_client.logger
        )

    @allure.story('Создание сущности')
    @allure.title('Проверка создания новой сущности')
    def test_create_entity(
        self,
        logger,
        teardown_entity
    ):
        api_client = ApiClient(logger=logger)
        api_client.create_entity(DataHelper.entity_setup_data())
        teardown_entity['id'] = api_client.response_data
        ValidationHelper.validate_via_pydantic(
            EntityCreateModel,
            api_client.response_data,
            api_client.logger
        )
        assert api_client.response_data in api_client.get_entities_id_list()

    @allure.story('Редактирование сущности')
    @allure.title('Проверка редактирования сущности')
    def test_edit_entity(
        self,
        setup_and_teardown_entity,
        logger
    ):
        api_client = ApiClient(logger=logger)
        entity_data = DataHelper.entity_setup_data()
        original_title = entity_data['title']
        api_client.patch_entity(
            entity_data,
            setup_and_teardown_entity
        )
        AssertionHelper.check_patched_entity_title(
            setup_and_teardown_entity,
            original_title,
            api_client.logger
        )

    @allure.story('Удаление сущности')
    @allure.title('Проверка удаления сущности')
    def test_delete_entity(
        self,
        created_entity_id,
        logger
    ):
        api_client = ApiClient(logger=logger)
        api_client.delete_entity(created_entity_id)
        AssertionHelper.check_delited_entity(
            created_entity_id,
            api_client.get_entities_id_list()
        )
