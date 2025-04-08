import logging
from logging import Logger
from datetime import datetime
from .api import Trading212API
from typing import Union

logger: Logger = logging.getLogger(__package__)


class Order:
    """
    Class representing a Trading212 order

    Methods
    -------
    update_properties
        uses the Trading212 object to call the Trading212 API and return the current order.
    """

    def __init__(
        self, api: Trading212API, data: dict[str, Union[str, int, float]]
    ) -> None:
        """
        Constructs an Trading212 order object representing the order

        Parameters
        ----------
        api (Trading212):Trading212API object used to call the Trading212 API
        data (dict):Data returned from the Trading212 API showing the details of the order
        """
        self._api: Trading212API = api
        self._update_order(data)

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def filled_quantity(self) -> float:
        return self._filled_quantity

    @property
    def filled_value(self) -> float:
        return self._filled_value

    @property
    def api(self) -> Trading212API:
        return self._api

    @property
    def id(self) -> int:
        return self._id

    @property
    def limit_price(self) -> float:
        return self._limit_price

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def status(self) -> str:
        return self._status

    @property
    def stop_price(self) -> float:
        return self._stop_price

    @property
    def strategy(self) -> str:
        return self._strategy

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> float:
        return self._value

    @property
    def creation_time(self) -> datetime:
        return self._creation_time

    def _update_order(self, data: dict[str, Union[str, int, float]]) -> None:
        self._ticker: str = data["ticker"]
        self._filled_quantity: float = data["filledQuantity"]
        self._filled_value: float = data["filledValue"]
        self._creation_time: datetime = datetime.fromisoformat(data["creationTime"])
        self._id: int = data["id"]
        self._limit_price: float = data["limitPrice"]
        self._quantity: float = data["quantity"]
        self._status: str = data["status"]
        self._stop_price: float = data["stopPrice"]
        self._strategy: str = data["strategy"]
        self._type: str = data['type']
        self._value: float = data['value']

    async def update_data(
        self,
    ) -> None:
        """
        Calls the Trading 212 api to update the order.

        Returns
        -------
        None
        """
        logger.info(f"Updating order for {self.id}")
        data = await self._api.get_orders(order=self._id)

        self._update_order(data)
