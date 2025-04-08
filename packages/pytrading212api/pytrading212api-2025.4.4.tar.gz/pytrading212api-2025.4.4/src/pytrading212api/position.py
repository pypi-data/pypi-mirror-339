import logging
from logging import Logger
from datetime import datetime
from .api import Trading212API
from typing import Union

logger: Logger = logging.getLogger(__package__)


class Position:
    """
    Class representing a Trading212 position

    Methods
    -------
    update_properties
        uses the Trading212 object to call the Trading212 API and return the current position.
    """

    def __init__(
        self, api: Trading212API, data: dict[str, Union[str, int, float]]
    ) -> None:
        """
        Constructs an Trading212 Position object representing the position

        Parameters
        ----------
        api (Trading212):Trading212API object used to call the Trading212 API
        data (dict):Data returned from the Trading212 API showing the details of the position
        """
        self._api: Trading212API = api
        self._update_position(data)

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def average_price(self) -> float:
        return self._average_price

    @property
    def api(self) -> Trading212API:
        return self._api

    @property
    def current_price(self) -> float:
        return self._current_price

    @property
    def profit_loss(self) -> float:
        return self._profit_loss

    @property
    def foreign_exchange_profit_loss(self) -> float:
        return self._foreign_exchange_profit_loss

    @property
    def initial_fill_date(self) -> datetime:
        return self._initial_fill_date

    @property
    def frontend(self) -> str:
        return self._frontend

    @property
    def max_buy(self) -> float:
        return self._max_buy

    @property
    def max_sell(self) -> float:
        return self._max_sell

    @property
    def pie_quantity(self) -> int:
        return self._pie_quantity
    
    @property
    def buy_value(self) -> float:
        return self._buy_value
    
    @property
    def current_value(self) -> float:
        return self._current_value
    
    @property
    def percent_change(self) -> float:
        return self._percent_change

    def _update_position(self, data: dict[str, Union[str, int, float]]) -> None:
        self._ticker: str = data["ticker"]
        self._quantity: float = data["quantity"]
        self._average_price: float = data["averagePrice"]
        self._current_price: float = data["currentPrice"]
        self._profit_loss: float = data["ppl"]
        self._foreign_exchange_profit_loss: float = data["fxPpl"]
        self._initial_fill_date: datetime = datetime.fromisoformat(data["initialFillDate"])
        self._frontend: str = data["frontend"]
        self._max_buy: float = data["maxBuy"]
        self._max_sell: float = data["maxSell"]
        self._pie_quantity: float = data["pieQuantity"]
        self._buy_value: float = self._average_price * self._quantity
        self._current_value: float = self._current_price * self._quantity
        self._percent_change: float = round((self._profit_loss/self._buy_value)*100,2) if self._buy_value else 0.0

    async def update_data(
        self,
    ) -> None:
        """
        Calls the Trading 212 api to update the position.

        Returns
        -------
        None
        """
        logger.info(f"Updating position for {self.ticker}")
        data = await self._api.get_positions(ticker=self._ticker)

        self._update_position(data)
