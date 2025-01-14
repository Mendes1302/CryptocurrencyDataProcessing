import requests
from datetime import datetime
from typing import Optional, Dict, Any

class CoinCapAPI():
    """
    A class to interact with the CoinCap API for cryptocurrency data.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the CoinCapAPI instance.
        ------------------------------------

        Args:
            api_key (str, optional): The API key for authentication. Defaults to None.
        """
        self.__base_url = "https://api.coincap.io/v2"
        self.__api_key = api_key

    def __build_headers(self) -> Dict[str, str]:
        """
        Builds HTTP headers for API requests.

        Returns:
            Dict[str, str]: A dictionary containing the request headers.
        """
        headers = {"Accept": "application/json"}
        if self.__api_key: headers["Authorization"] = f"Bearer {self.__api_key}"
        return headers

    def get_crypto_by_id(self, crypto_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches details of a specific cryptocurrency by its ID.
        -------------------------------------------------------

        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').

        Returns:
            Optional[Dict[str, Any]]: The cryptocurrency data as a dictionary, 
            or None if the request fails.
        """
        try:
            response = requests.get(
                f"{self.__base_url}/assets/{crypto_id}",
                headers=self.__build_headers()
            )
            response.raise_for_status()
            return response.json().get("data", None)
        except requests.RequestException as e:
            print(f"Error accessing API data for {crypto_id}: {e}")
            return None

    def get_price_history(self, crypto_id: str, start_date: datetime, end_date: datetime) -> Optional[Dict[str, Any]]:
        """
        Retrieves the historical price data of a cryptocurrency within a specified date range.
        -------------------------------------------------------------------------------------

        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
            start_date (datetime): The start date for the historical data.
            end_date (datetime): The end date for the historical data.

        Returns:
            Optional[Dict[str, Any]]: The price history data as a dictionary,
            or None if the request fails.
        """
        try:
            start_timestamp = int(start_date.timestamp() * 1000)
            end_timestamp = int(end_date.timestamp() * 1000)
            response = requests.get(
                f"{self.__base_url}/assets/{crypto_id}/history",
                params={"interval": "d1", "start": start_timestamp, "end": end_timestamp},
                headers=self.__build_headers()
            )
            response.raise_for_status()
            return response.json().get("data", None)
        except requests.RequestException as e:
            print(f"Error accessing price history for {crypto_id}: {e}")
            return None
        

    def get_market_details(self, crypto_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed market information for a specific cryptocurrency by its ID.

        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').

        Returns:
            Optional[Dict[str, Any]]: Market details, including 24-hour volume and price trends.
        """
        try:
            response = requests.get(
                f"{self.__base_url}/assets/{crypto_id}/markets",
                headers=self.__build_headers(),
                params={"limit": 2000}
            )
            response.raise_for_status()
            return response.json().get("data", None)
        except requests.RequestException as e:
            print(f"Error accessing market details for {crypto_id}: {e}")
            return None