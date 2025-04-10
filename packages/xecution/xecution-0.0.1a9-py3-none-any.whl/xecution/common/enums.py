from enum import Enum

class KlineType(Enum):
    Binance_Spot = 1
    Binance_Futures = 2
    Bybit_Spot = 3
    Bybit_Futures = 4
    OKX_Spot = 5
    OKX_Futures = 6

class Mode(Enum):
    Live = 1
    Backtest = 2
    Testnet = 3
    
class ConcurrentRequest(Enum):
    Max = 3
    Chunk_Size = 5
    
class Exchange(Enum):
    Binance = 1
    Bybit = 2
    Okx = 3    
    
class Symbol(Enum):
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    SOLUSDT = "SOLUSDT"
    