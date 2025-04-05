import allure
import pytest

from api_client.api_client import ApiClient
from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from schemas.schemas import EntityCreateModel, EntityListModel, EntityModel


@allure.epic('SimbirSoft SDET practicum')
@allure.suite('API tests')
class TestApi:

    @allure.story('Получение сущности')
    @allure.title('Проверка получения сущности по ID')
    def test_get_entity(self, new_entity):
        api_client = ApiClient()
        response = api_client.get_entity_by_id(new_entity['id'])
        assert response.status_code == 200, \
            f'Excepted status code 200, got {response.status_code}'
        ValidationHelper.validate_via_pydantic(
            EntityModel,
            response.json(),
        )
        assert new_entity == response.json(), \
            'Значения полей новой сущности не равны передаваемым значениям полей'

    @pytest.mark.parametrize('new_entity', [3], indirect=True)
    @allure.story('Получение списка сущностей')
    @allure.title('Проверка получения списка сущностей')
    def test_get_entity_list(self, new_entity):
        api_client = ApiClient()
        response = api_client.get_entity_list()
        assert response.status_code == 200, \
            f'Excepted status code 200, got {response.status_code}'
        ValidationHelper.validate_via_pydantic(
            EntityListModel,
            response.json(),
        )
        AssertionHelper.check_getting_created_enity_data(new_entity, response.json()['entity'])

    @allure.story('Создание сущности')
    @allure.title('Проверка создания новой сущности')
    def test_create_entity(
        self,
        teardown_entity
    ):
        api_client = ApiClient()
        response = api_client.create_entity(DataHelper.entity_setup_data())
        teardown_entity.append(response.json())
        assert response.status_code == 200, \
            f'Excepted status code 200, got {response.status_code}'
        ValidationHelper.validate_via_pydantic(
            EntityCreateModel,
            response.json()
        )
        assert response.json() in api_client.get_entities_id_list()

    @allure.story('Редактирование сущности')
    @allure.title('Проверка редактирования сущности')
    def test_edit_entity(
        self,
        new_entity,
    ):
        api_client = ApiClient()
        entity_data = DataHelper.entity_setup_data()
        original_title = entity_data['title']
        response = api_client.patch_entity(
            entity_data,
            new_entity['id']
        )
        assert response.status_code == 204, \
            f'Excepted status code 204, got {response.status_code}'
        assert AssertionHelper.get_entity_title(new_entity['id']) == f'EDITED_{original_title}', \
            f'New entity title  must be "EDITED_{original_title}'

    @allure.story('Удаление сущности')
    @allure.title('Проверка удаления сущности')
    def test_delete_entity(
        self,
        created_entity_id,
    ):
        api_client = ApiClient()
        response = api_client.delete_entity(created_entity_id)
        assert response.status_code == 204, \
            f'Excepted status code 204, got {response.status_code}'
        AssertionHelper.check_delited_entity(
            created_entity_id,
            api_client.get_entities_id_list()
        )
