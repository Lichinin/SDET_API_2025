from pathlib import Path


class Paths:
    LOG_DIR = Path(__file__).parent / 'log'


class APiRoutes:

    BASE_URL = 'http://localhost:8080'
    API_VER = '/api'
