import logging

from sven.config import settings

from .agent import Agent
from .api import Api


class ApiClient:
    def __init__(self, api_url: str | None = None, api_key: str | None = None):
        _api_url = api_url or settings.api_url
        _api_key = api_key or settings.api_key
        self.api = Api(_api_url, _api_key)
        self.agent = Agent(self.api)

        logging.info(f"API URL: {_api_url}")
