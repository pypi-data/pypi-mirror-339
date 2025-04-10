import time

import requests

from src.app.config.app_data import APP_NAME, APP_VERSION
from src.app.config.logger import logger


class ScryfallUtils:
    @classmethod
    def headers(cls: "ScryfallUtils") -> dict:
        """Build headers for the Scryfall API request.

        Returns:
            dict: A dictionary containing the User-Agent and Accept headers for the API request.
        """
        return {
            "User-Agent": f"{APP_NAME}/{APP_VERSION}",
            "Accept": "application/json;q=0.9,*/*;q=0.8",
        }

    @classmethod
    def call_scryfall_api(cls: "ScryfallUtils", link: str) -> dict:
        """Query the Scryfall API to retrieve first prints card data.

        Args:
            link (str): The Scryfall API link to query. If not provided, a default query string will be used.

        Returns:
            dict: A dictionary containing the card data retrieved from the Scryfall API, including 'data' and 'has_more' keys.

        Raises:
            requests.exceptions.RequestException: If the API request fails.

        """
        time.sleep(0.2)  # Mandatory rest requested by Scryfall's API

        try:
            logger.debug(f"Scyrfall API call: {link}")
            response = requests.get(link, stream=True, headers=cls.headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Scryfall API request failed: {e}")
            return {"data": [], "has_more": False}
