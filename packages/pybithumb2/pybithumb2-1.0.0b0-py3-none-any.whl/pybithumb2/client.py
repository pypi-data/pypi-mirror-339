from typing import List, Optional, Union, Set
from datetime import datetime, time
from decimal import Decimal

from pybithumb2.__env__ import API_BASE_URL
from pybithumb2.types import (
    RawData,
    Currency,
    OrderID,
    OrderState,
    OrderType,
    OrderBy,
    TradeSide,
)
from pybithumb2.models import (
    Account,
    DFList,
    MarketID,
    Market,
    MinuteCandle,
    DayCandle,
    WeekCandle,
    MonthCandle,
    TimeUnit,
    TradeInfo,
    Snapshot,
    OrderBook,
    OrderAvailable,
    OrderInfo,
    Order,
    WarningMarketInfo,
    WalletStatus,
    APIKeyInfo,
)
from pybithumb2.rest import RESTClient
from pybithumb2.exceptions import APIError
from pybithumb2.utils import clean_and_format_data


class BithumbClient(RESTClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        use_raw_data: bool = False,
    ) -> None:
        """
        Instantiates the Bithumb Client.
        If either key is missing, then the client will only have access to the public API.

        Args:
            api_key (str, optional): The API key for the client.
            secret_key (str, optional): The secret key for the client.
            use_raw_data (bool): Whether the API response is returned as raw data or in pydantic models.
        """
        super().__init__(API_BASE_URL, api_key, secret_key, use_raw_data)

    # ##### Public API features #####
    def get_markets(self, isDetails: bool = False) -> Union[List[Market], RawData]:
        """
        Instantiates the Bithumb Client.
        If either key is missing, then the client will only have access to the public API.

        Args:
            isDetails (bool): Whether the API response is returned as raw data or in pydantic models. Defaults to False.

        Returns:
            Union[List[Market], RawData]
        """
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/market/all", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return [Market.model_validate(item) for item in response]

    def get_minute_candles(
        self,
        market: MarketID,
        to: Optional[datetime] = None,
        count: int = 1,
        unit: TimeUnit = TimeUnit(1),
    ) -> Union[DFList[MinuteCandle], RawData]:
        if count <= 0 or count > 200:
            raise APIError("You can only request betwewen 1 and 200 candles")

        data = locals().copy()
        data.pop("self")
        data.pop("unit")
        data = clean_and_format_data(data)

        response = self.get(f"/v1/candles/minutes/{unit}", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[MinuteCandle](
            [MinuteCandle.model_validate(item) for item in response]
        )

    def get_day_candles(
        self,
        market: MarketID,
        to: Optional[datetime] = None,
        count: int = 1,
        convertingPriceUnit: Optional[Currency] = None,
    ) -> Union[DFList[DayCandle], RawData]:
        if count <= 0 or count > 200:
            raise APIError("You can only request betwewen 1 and 200 candles")
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/candles/days", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[DayCandle]([DayCandle.model_validate(item) for item in response])

    def get_week_candles(
        self, market: MarketID, to: Optional[datetime] = None, count: int = 1
    ) -> Union[DFList[WeekCandle], RawData]:
        if count <= 0 or count > 200:
            raise APIError("You can only request betwewen 1 and 200 candles")
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/candles/weeks", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[WeekCandle](
            [WeekCandle.model_validate(item) for item in response]
        )

    def get_month_candles(
        self, market: MarketID, to: Optional[datetime] = None, count: int = 1
    ) -> Union[DFList[MonthCandle], RawData]:
        if count <= 0 or count > 200:
            raise APIError("You can only request betwewen 1 and 200 candles")
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/candles/weeks", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[MonthCandle](
            [MonthCandle.model_validate(item) for item in response]
        )

    def get_trades(
        self,
        market: MarketID,
        to: Optional[time] = None,
        count: int = 1,
        # cursor: str, # No support for this yet. (I don't know what its supposed to do)
        daysAgo: Optional[int] = None,
    ) -> Union[TradeInfo, RawData]:
        if daysAgo is not None and (daysAgo <= 0 or daysAgo > 7):
            raise APIError("You can only request data from 1 to 7 days ago")
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/trades/ticks", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[TradeInfo]([TradeInfo.model_validate(item) for item in response])

    def get_snapshots(
        self, markets: List[MarketID]
    ) -> Union[DFList[Snapshot], RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/ticker", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return DFList[Snapshot]([Snapshot.model_validate(item) for item in response])

    def get_orderbooks(
        self, markets: List[MarketID]
    ) -> Union[List[OrderBook], RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/orderbook", is_private=False, data=data)

        if self._use_raw_data:
            return response

        return [OrderBook(**item) for item in response]

    def get_warning_markets(self) -> Union[List[WarningMarketInfo], RawData]:
        response = self.get("/v1/market/virtual_asset_warning", is_private=False)

        if self._use_raw_data:
            return response

        return [WarningMarketInfo.model_validate(item) for item in response]

    # ##### Private API features #####
    def get_accounts(self) -> Union[List[Account], RawData]:
        response = self.get("/v1/accounts", is_private=True)

        if self._use_raw_data:
            return response

        return [Account.model_validate(item) for item in response]

    def get_order_available(self, market: MarketID) -> Union[OrderAvailable, RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/orders/chance", is_private=True, data=data)

        if self._use_raw_data:
            return response

        return OrderAvailable.model_validate(response)

    def get_order_info(
        self, uuid: Optional[OrderID] = None
    ) -> Union[DFList[OrderInfo], RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.get("/v1/orders", is_private=True, data=data)

        if self._use_raw_data:
            return response

        return DFList[OrderInfo]([OrderInfo.model_validate(item) for item in response])

    def get_orders(
        self,
        market: MarketID,
        uuids: Optional[List[OrderID]] = None,
        state: Optional[OrderState] = None,
        states: Optional[Set[OrderState]] = None,
        page: int = 1,
        limit: int = 100,
        order_by: OrderBy = OrderBy.DESC,
    ) -> Union[DFList[Order], RawData]:
        if states:
            if state:
                raise AssertionError("You can not have both state and states parameter")

        data = locals().copy()
        data.pop("self")
        data.pop("uuids")
        data = clean_and_format_data(data)
        if uuids:
            data["uuids"] = [str(u.id) for u in uuids]

        response = self.get("/v1/orders", is_private=True, data=data, doseq=True)

        if self._use_raw_data:
            return response

        return DFList[Order]([Order.model_validate(item) for item in response])

    def cancel_order(self, uuid: OrderID) -> Union[Order, RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.delete("/v1/order", is_private=True, data=data)

        if self._use_raw_data:
            return response
        return Order.model_validate(response)

    def submit_order(
        self,
        market: MarketID,
        side: TradeSide,
        volume: Decimal,
        price: Decimal,
        ord_type: OrderType,
    ) -> Union[Order, RawData]:
        data = locals().copy()
        data.pop("self")
        data = clean_and_format_data(data)

        response = self.post("/v1/orders", is_private=True, data=data)

        if self._use_raw_data:
            return response

        return Order.model_validate(response)

    def get_wallet_status(self) -> Union[DFList[WalletStatus], RawData]:
        response = self.get("/v1/status/wallet", is_private=True)

        if self._use_raw_data:
            return response

        return DFList[WalletStatus](
            [WalletStatus.model_validate(item) for item in response]
        )

    def get_api_keys(self) -> Union[DFList[APIKeyInfo], RawData]:
        response = self.get("/v1/api_keys", is_private=True)

        if self._use_raw_data:
            return response

        return DFList[APIKeyInfo](
            [APIKeyInfo.model_validate(item) for item in response]
        )
