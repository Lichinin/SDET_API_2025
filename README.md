# SDET_API_2025
[![Run Tests](https://github.com/Lichinin/SDET_API_2025/actions/workflows/main.yml/badge.svg)](https://github.com/Lichinin/SDET_API_2025/actions/workflows/main.yml)

**Автор:** Виталий Личинин  
**Репозиторий:** [GitHub](https://github.com/Lichinin/SDET_API_2025)

## Оглавление
1. [Цели проекта](#цели-проекта)
2. [Технологии](#используемые-технологии)
3. [Структура проекта](#структура-проекта)
4. [Запуск тестов](#запуск-проекта)
5. [Пример логов тестов](#примеры-логов)
6. [Примеры отчетов](#примеры-отчетности-allure)

---

## Цели проекта
- Автоматизация тестирования REST API
- Реализация клиента API
- Интеграция Allure для отчетности
- Настройка CI/CD через GitHub Actions
- Генерация тестовых данных с Faker
- Валидация схем ответа API
- Настройка pre-commit хуков для контроля качества кода

## Используемые технологии

| Компонент         | Версия    | Назначение                          |
|-------------------|-----------|-------------------------------------|
| python            | 3.10      | Базовый язык                        |
| pytest            | 8.3.5     | Фреймворк для тестирования          |
| requests          | 2.32.3    | HTTP-запросы к API                  |
| pydantic          | 2.11.1    | Валидация данных                    |
| allure-pytest     | 2.13.5    | Генерация отчетов Allure            |
| Faker             | 37.1.0    | Генерация тестовых данных           |
| flake8            | 7.2.0     | Линтер для проверки стиля кода      |
| pytest-xdist      | 3.6.1     | Параллельный запуск тестов          |
| pre_commit        | 4.2.0     | Автоматизация проверок перед коммитом|

## Структура проекта

├─ allure-result                          
├─ api_client             
│  ├─ api_client.py       
│  └─ base_api_client.py  
├─ helpers                
│  ├─ api_helpers.py      
│  └─ data_helpers.py
├─ logs
├─ schemas                
│  └─ schemas.py          
├─ tests                  
│  ├─ test_api            
│  │  └─ test_api.py      
│  └─ conftest.py         
├─ config.py              
├─ pytest.ini             
├─ README.md              
└─ requirements.txt       

### Описание папок
- **allure-results** -  результаты для генерации Allure-отчетов
- **api_client** - содержит реализацию клиента для работы с API
- **helpers** - вспомогательные функции для тестов
- **logs** - логи выполнения тестов (автогенерация) 
- **schemas** - модели данных для валидации ответов API
- **tests** - тестовые сценарии с использованием pytest

### Ключевые файлы
- **api_client.py** - основной клиент для работы с API
- **schemas.py** - модели Pydantic для валидации ответов
- **conftest.py** - фикстуры для управления тестовыми данными
- **data_helpers.py** - генератор тестовых данных

## Запуск проекта

### Установка зависимостей
```bash
git clone https://github.com/Lichinin/SDET_API_2025.git
cd SDET_API_2025
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
**Стандартный запуск**
```
pytest
```

**Параллельный запуск (3 потока)**
```
pytest -n 3
```

### Примеры логов.
***test_create_entity.log***
```
2025-04-06 20:35:04,725 - test_create_entity - INFO - Test started: test_create_entity
2025-04-06 20:35:04,728 - ApiClient - INFO - Send POST request to http://localhost:8080/api/create
2025-04-06 20:35:04,742 - validation.EntityCreateModel - INFO - * Check response scheme
2025-04-06 20:35:04,743 - validation.EntityCreateModel - INFO - entity data: 125
2025-04-06 20:35:04,743 - validation.EntityCreateModel - INFO - * Scheme is valid.
2025-04-06 20:35:04,744 - ApiClient - INFO - Send GET request to http://localhost:8080/api/getALL
2025-04-06 20:35:04,758 - fixture.test_create_entity - INFO - ====> Fixture: Delete entity for test
2025-04-06 20:35:04,759 - ApiClient - INFO - Send DELETE request to http://localhost:8080/api/delete/125
2025-04-06 20:35:04,773 - test_create_entity - INFO - Test finished: test_create_entity
```

**test_get_entity.log**
```
2025-04-06 20:51:31,602 - test_get_entity - INFO - Test started: test_get_entity
2025-04-06 20:51:31,603 - fixture.test_get_entity - INFO - ====> Fixture setup started
2025-04-06 20:51:31,604 - fixture.test_get_entity - INFO - ====> Fixture: Try create entity for test
2025-04-06 20:51:31,605 - ApiClient - INFO - Send POST request to http://localhost:8080/api/create
2025-04-06 20:51:31,628 - fixture.test_get_entity - INFO - ====> Fixture: Successful create entity (id=128) for test.
2025-04-06 20:51:31,629 - ApiClient - INFO - Send GET request to http://localhost:8080/api/get/128
2025-04-06 20:51:31,642 - ApiClient - INFO - Send GET request to http://localhost:8080/api/get/128
2025-04-06 20:51:31,651 - validation.EntityModel - INFO - * Check response scheme
2025-04-06 20:51:31,652 - validation.EntityModel - INFO - entity data: {'id': 128, 'title': 'Decade story.', 'verified': True, 'addition': {'id': 128, 'additional_info': 'Defense expect single.', 'additional_number': 6}, 'important_numbers': [10, 67, 89]}
2025-04-06 20:51:31,652 - validation.EntityModel - INFO - * Scheme is valid.
2025-04-06 20:51:31,656 - fixture.test_get_entity - INFO - ====> Fixture: Delete entity (id=128) for test
2025-04-06 20:51:31,657 - ApiClient - INFO - Send DELETE request to http://localhost:8080/api/delete/128
2025-04-06 20:51:31,667 - fixture.test_get_entity - INFO - ====> Fixture setup exit
2025-04-06 20:51:31,672 - test_get_entity - INFO - Test finished: test_get_entity
```

### Примеры отчетности Allure.

Для просмотра отчетов:
```
allure serve allure-results
```
* Summary по тестам:

* Тесткейсы:

* Пример отчета по тесткейсу:
