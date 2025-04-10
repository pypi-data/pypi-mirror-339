import logging
from xecution.models.config import RuntimeConfig,OrderConfig
from xecution.models.topic import KlineTopic
from xecution.services.connection.base_websockets import WebSocketService
from xecution.services.exchange.binance_helper import BinanceHelper
from xecution.common.enums import Mode, Symbol
from xecution.services.exchange.exchange_order_manager import BinanceOrderManager

class BinanceService:
    
    def __init__(self, config: RuntimeConfig, data_map: dict):
        """
        Binance Service for managing WebSocket and API interactions.
        """
        self.config = config
        self.ws_service = WebSocketService()
        self.data_map = data_map  # External data map reference
        self.binanceHelper = BinanceHelper(self.config)
        self.manager = BinanceOrderManager(
            api_key=config.API_Key,
            api_secret=config.API_Secret,
            mode = config.mode
        )
        
    async def check_connection(self):
        account_info = await self.get_account_info()
        if not account_info or "code" in account_info:  # Binance 錯誤回應通常有 "code"
            error_msg = account_info.get("msg", "Unknown error") if account_info else "No response"
            logging.error(f"[BinanceService] check_connection : API Key validation failed: {error_msg}")
            # Raise an exception to signal failure
            raise ConnectionError(f"API Key validation failed: {error_msg}")
        logging.info(f"[BinanceService] check_connection : Successfully connected to Binance")
    
    async def get_klines(self,on_candle_closed):
        """
        呼叫 Binance /api/v3/klines 取得 K 線
        """
        for kline_topic in self.config.kline_topic :
            if self.config.mode == Mode.Backtest:
                candles = await self.binanceHelper.getKlineRestAPI(kline_topic)
                self.data_map[kline_topic] = candles
                await on_candle_closed(kline_topic)
            elif self.config.mode == Mode.Live or self.config.mode == Mode.Testnet:
                await self.listen_kline(on_candle_closed,kline_topic)

    async def listen_kline(self, on_candle_closed, kline_topic: KlineTopic):
        """Subscribe to Binance WebSockets, receive messages, and send closed candles to `on_candle_closed`."""
        try:
            def get_connection_urls():
                """Generate WebSocket connection URLs using `RuntimeConfig.kline_topic`."""
                try:
                    connection_urls = {}
                    kline_topic_mapping = {}  # Store kline_topic info for mapping
                    ws_url = self.binanceHelper.get_websocket_base_url(kline_topic,self.config.mode) + f"/{kline_topic.symbol.lower()}@kline_{kline_topic.timeframe.lower()}"
                    connection_urls[ws_url] = (ws_url, None)  # No extra subscription message needed
                    kline_topic_mapping[ws_url] = kline_topic  # Maps WebSocket URL to kline_topic
                    # Ensure external data_map stores kline_topic keys
                    self.data_map[kline_topic] = []
                    return connection_urls, kline_topic_mapping
                except Exception as e:
                    logging.error(f"[BinanceService] get_connection_urls failed: {e}")

            async def message_handler(exchange, message):
                """Processes incoming kline messages and calls `on_candle_closed` with `kline_topic` only."""
                try:
                    kline = message.get("k", {})
                    if not kline:
                        return  # Ignore invalid messages
                    is_closed = kline.get("x", False)  # Ensure candle is fully closed
                    if not is_closed:
                        return  # Skip unfinished candles
                    # Extract kline_topic from mapping
                    ws_url = message.get("s")  # Get symbol from message
                    kline_topic = next((kt for kt in self.config.kline_topic if ws_url == kt.symbol), None)
                    if not kline_topic:
                        logging.warning(f"[BinanceService][{exchange}] Kline topic mapping not found for {ws_url}. Skipping message.")
                        return
                    # call get_kline_restapi
                    while True:
                        candles = await self.binanceHelper.getLatestKline(kline_topic)
                        ws_start_time = self.binanceHelper.convert_ws_kline(kline).get("start_time")

                        if candles["start_time"] == ws_start_time:
                            # Found matching candle
                            self.data_map[kline_topic] = await self.binanceHelper.getKlineRestAPI(kline_topic)
                            break

                    logging.debug(f"[{exchange}] Candle Closed | {kline_topic.symbol}-{kline_topic.timeframe} | Close: {kline.get('c')}")
                    # Only pass `kline_topic` to `on_candle_closed`
                    await on_candle_closed(kline_topic)
                    
                except Exception as e:
                    logging.error(f"[BinanceService] message_handler failed: {e}")

            # Establish WebSocket connections
            connection_urls, kline_topic_mapping = get_connection_urls()
            for exchange_name, (ws_url, subscription_message) in connection_urls.items():
                logging.debug(f"Connecting to {ws_url}")
                await self.ws_service.subscribe(exchange_name, ws_url, subscription_message, message_handler)

            logging.info("[BinanceService] WebSocket connections initialized.")
        except Exception as e:
            logging.error(f"[BinanceService] listen_kline failed: {e}")
        

    async def place_order(self, order_config: OrderConfig):
        # 檢查是否已有未成交訂單，避免重複下單
        await self.manager.place_order(order_config)
        
    async def get_account_info(self):
        account_info = await self.manager.get_account_info()
        return account_info
    
    async def get_wallet_balance(self):
        wallet_balance = await self.manager.get_wallet_balance()
        return wallet_balance
    
    async def set_hedge_mode(self,is_hedge_mode: bool):
        await self.manager.set_hedge_mode(is_hedge_mode) 
        
    async def set_leverage(self,symbol: str, leverage: int):
        await self.manager.set_leverage(symbol,leverage)
    
    async def get_position_info(self, symbol: Symbol):
        return await self.manager.get_position_info(symbol)

    async def get_current_price(self,symbol: str):
        return await self.manager.get_current_price(symbol)
    
    async def get_order_book(self,symbol:Symbol):
        orderbook  = self.binanceHelper.parse_order_book(await self.manager.get_order_book(symbol)) 
        logging.info(f"[BinanceService] get_order_book: {orderbook}")
        return orderbook
