import allure
import pytest

from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from schemas.schemas import EntityCreateModel, EntityListModel, EntityModel


@allure.epic('SimbirSoft SDET practicum')
@allure.suite('API tests')
class TestApi:

    @allure.story('Получить сущность')
    @allure.title('Проверка получения сущности по ID')
    def test_get_entity(self, api_client, new_entity):
        response = api_client.get_entity_by_id(new_entity['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                EntityModel,
                response.json(),
            )
        with allure.step('Сравнить значения полей полученной сущности с тестовыми данными.'):
            assert new_entity == response.json(), (
                'Значения полей новой сущности не равны передаваемым значениям полей. '
                f'Ожидается: {new_entity}.Получено: {response.json()}'
            )

    @pytest.mark.parametrize('new_entity', [3], indirect=True)
    @allure.story('Получить список всех сущностей')
    @allure.title('Проверка получения списка всех сущностей')
    def test_get_entity_list(self, api_client, new_entity):
        response = api_client.get_entity_list()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                EntityListModel,
                response.json(),
            )
        with allure.step('Проверить, что созданные тестовые сущности есть в списке всех сущностей'):
            AssertionHelper.check_getting_created_entity_data(new_entity, response.json()['entity'])

    @allure.story('Создание сущности')
    @allure.title('Проверка создания новой сущности')
    def test_create_entity(self, api_client, teardown_entity):
        response = api_client.create_entity(DataHelper.entity_setup_data())
        teardown_entity.append(response.json())
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                EntityCreateModel,
                response.json()
            )
        with allure.step('Проверить, что созданная сущность существует в базе данных'):
            AssertionHelper.check_status_code(
                api_client.get_entity_by_id(response.json()).status_code,
                200
            )

    @allure.story('Редактирование сущности')
    @allure.title('Проверка редактирования сущности')
    def test_edit_entity(self, api_client, new_entity):
        entity_data = DataHelper.entity_setup_data()
        original_title = entity_data['title']
        entity_data['title'] = f'EDITED_{entity_data["title"]}'
        response = api_client.patch_entity(
            entity_data,
            new_entity['id']
        )
        AssertionHelper.check_status_code(response.status_code, 204)
        with allure.step('Проверить, что "title" сущности соответствует измененному значению'):
            assert AssertionHelper.get_entity_title(new_entity['id']) == f'EDITED_{original_title}', (
                f'Измененный "title" сущности должен быть равен "EDITED_{original_title}"'
            )

    @allure.story('Удаление сущности')
    @allure.title('Проверка удаления сущности')
    def test_delete_entity(self, api_client, created_entity_id):
        response = api_client.delete_entity(created_entity_id)
        AssertionHelper.check_status_code(response.status_code, 204)
        with allure.step('Проверить, удаленная сущность отсутствует в списке всех сущностей'):
            AssertionHelper.check_deleted_entity(
                created_entity_id,
                api_client.get_entities_id_list()
            )
