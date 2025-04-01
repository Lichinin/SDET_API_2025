from pathlib import Path


class Pathes:
    LOG_DIR = Path(__file__).parent / 'log'


class APiRoutes:

    BASE_URL = 'http://localhost:8080'
    API_VER = '/api'

    @classmethod
    def entity_by_id_url(cls, entity_id):
        return f'{cls.BASE_URL}{cls.API_VER}/get/{entity_id}'

    @classmethod
    def entity_list_url(cls):
        return f'{cls.BASE_URL}{cls.API_VER}/getALL'

    @classmethod
    def create_entity_url(cls):
        return f'{cls.BASE_URL}{cls.API_VER}/create'

    @classmethod
    def patch_entity_url(cls, entity_id):
        return f'{cls.BASE_URL}{cls.API_VER}/patch/{entity_id}'

    @classmethod
    def delete_entity_url(cls, entity_id):
        return f'{cls.BASE_URL}{cls.API_VER}/delete/{entity_id}'
