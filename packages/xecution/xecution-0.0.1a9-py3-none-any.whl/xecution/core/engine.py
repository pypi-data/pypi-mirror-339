import asyncio
import logging
import numpy as np
from datetime import datetime, timezone
from xecution.common.enums import Exchange, KlineType, Mode, Symbol
from xecution.models.config import OrderConfig, RuntimeConfig
from xecution.models.topic import KlineTopic
from xecution.services.exchange.binance_service import BinanceService
from xecution.services.exchange.bybit_service import BybitService
from xecution.services.exchange.okx_service import OkxService
from xecution.utils.logger import Logger

class BaseEngine:
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""

    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.data_map = {}  # Local data storage for kline data
        self.binance_service = BinanceService(config, self.data_map)  # Pass data_map to BinanceService
        self.bybit_service = BybitService(config, self.data_map)  # Pass data_map to BybitService
        self.okx_service = OkxService(config, self.data_map)  # Pass data_map to OkxService
        # Logger(log_file="my_strategy_log.log")

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data using `self.data_map[kline_topic]`."""
        
        # Ensure kline_topic exists in data_map
        if kline_topic not in self.data_map:
            logging.error(f"No candle data found for {kline_topic}")
            return
        
        # Access stored candle data
        candles = self.data_map[kline_topic]
        start_time = np.array([float(c["start_time"]) for c in candles])
        close = np.array([float(c["close"]) for c in candles])
        
        order_config = OrderConfig(
            market_type=KlineType.Binance_Futures,
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=1.5
        )
        await self.get_order_book(Symbol.ETHUSDT)
        await self.get_position_info(Symbol.BTCUSDT)
        await self.get_wallet_balance()
        await self.set_hedge_mode(False)
        await self.place_order(order_config)
        await self.set_leverage("BTCUSDT",100)
        await self.get_current_price("BTCUSDT")
        
        logging.info(f"candles data length: {len(candles)}")
        logging.info(
            f"Last Kline Closed | {kline_topic.symbol}-{kline_topic.timeframe} | Close: {close[-1]} | Time: {datetime.fromtimestamp(start_time[-1] / 1000)}"
        )

    async def on_datasource_update(self, datasource_topic):
        """Handles updates from external data sources."""
        logging.info(f"Datasource Updated | Topic: {datasource_topic}")

    async def start(self):
        """Starts BinanceService and behaves differently based on the runtime mode."""
        try:
            await self.binance_service.get_klines(self.on_candle_closed)

            if self.config.mode == Mode.Live or self.config.mode == Mode.Testnet:
                await self.binance_service.check_connection()
                while True:
                    await asyncio.sleep(1)  # Keep the loop alive
            else:
                logging.info("Backtest mode completed. Exiting.")
        except ConnectionError as e:
                logging.error(f"Connection check failed: {e}")
        
    async def place_order(self, order_config: OrderConfig):
        await self.binance_service.place_order(order_config)
        
    async def get_account_info(self):
        return await self.binance_service.get_account_info()

    async def set_hedge_mode(self, is_hedge_mode: bool):
        return await self.binance_service.set_hedge_mode( is_hedge_mode)

    async def set_leverage(self, symbol: str, leverage: int):
        return await self.binance_service.set_leverage(symbol, leverage)
    
    async def get_position_info(self, symbol: Symbol):
        return await self.binance_service.get_position_info(symbol)
    
    async def get_wallet_balance(self):
        return await self.binance_service.get_wallet_balance()

    async def get_current_price(self,symbol: str):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Bybit:
            return await self.bybit_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Okx:
            return await self.okx_service.get_current_price(symbol)
        else:
            logging.error("Unknown exchange")
            return None
    async def get_order_book(self,symbol:Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_order_book(symbol)
        else:
            logging.error("Unknown exchange")
            return None

if __name__ == "__main__":
    engine = BaseEngine(
        RuntimeConfig(
            mode= Mode.Testnet,
            kline_topic=[
                KlineTopic(klineType=KlineType.Binance_Futures, symbol="BTCUSDT", timeframe="1m"),
                # KlineTopic(klineType=KlineType.Binance_Futures, symbol="ETHUSDT", timeframe="1m"),
            ],
            start_time=datetime(2025,3,22,0,0,0,tzinfo=timezone.utc),
            data_count=100,
            exchange=Exchange.Binance,
            API_Key="0023f3dd37d75912abffc7a7bb95def2f7a1e924dc99b2a71814ada35b59dd15" ,  # Replace with your API Key if needed
            API_Secret="5022988215bffb0a626844e7b73125533d1776b723a2abe2a8d2f8440da378d9", # Replace with your API Secret if needed
        )
    )

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(engine.start())  # will exit automatically for backtest
    except KeyboardInterrupt:
        logging.info("Shutting down BinanceService...")
    finally:
        loop.close()

