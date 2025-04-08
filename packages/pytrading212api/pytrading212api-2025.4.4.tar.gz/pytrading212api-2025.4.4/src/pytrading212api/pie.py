import logging
from logging import Logger
from datetime import datetime
from .api import Trading212API
from typing import Any

logger: Logger = logging.getLogger(__package__)


class Pie:
    """
    Class representing a Trading212 pie

    Methods
    -------
    update_properties
        uses the Trading212 object to call the Trading212 API and return the current pie.
    """

    def __init__(
        self, api: Trading212API, data: dict[str, Any]
    ) -> None:
        """
        Constructs an Trading212 pie object representing the pie

        Parameters
        ----------
        api (Trading212):Trading212API object used to call the Trading212 API
        data (dict):Data returned from the Trading212 API showing the details of the pie
        """
        self._api: Trading212API = api
        self._update_pie(data)

    @property
    def id(self) -> int:
        return self._id

    @property
    def cash(self) -> float:
        return self._cash

    @property
    def progress(self) -> float:
        return self._progress

    @property
    def api(self) -> Trading212API:
        return self._api

    @property
    def status(self) -> str:
        return self._status

    @property
    def dividend_gained(self) -> float:
        return self._dividend_gained

    @property
    def dividend_cash(self) -> float:
        return self._dividend_cash

    @property
    def dividend_reinvested(self) -> float:
        return self._dividend_reinvested

    @property
    def average_price_invested_value(self) -> float:
        return self._average_price_invested_value

    @property
    def average_price(self) -> float:
        return self._average_price

    @property
    def average_price_coefficient(self) -> float:
        return self._average_price_coefficient

    @property
    def value(self) -> float:
        return self._value
    

    def _update_pie(self, data: dict[str, Any]) -> None:
        self._id: int = data["id"]
        self._cash: float = data["cash"]
        self._progress: float = data["progress"]
        self._status:str = data["status"]
        self._dividend_gained: float = data["dividendDetails"]["gained"]
        self._dividend_cash: float = data["dividendDetails"]["inCash"]
        self._dividend_reinvested: float = data["dividendDetails"]["reinvested"]
        self._average_price_invested_value: float = data["result"]["priceAvgInvestedValue"]
        self._average_price: float = data["result"]["priceAvgResult"]
        self._average_price_coefficient: float = data["result"]["priceAvgResultCoef"]
        self._value: float = data["result"]["priceAvgValue"]

    async def update_data(
        self,
    ) -> None:
        """
        Calls the Trading 212 api to update the pie.

        Returns
        -------
        None
        """
        logger.info(f"Updating pie for {self.id}")
        data = await self._api.get_pies(pie=self._id)

        self._update_pie(data)
